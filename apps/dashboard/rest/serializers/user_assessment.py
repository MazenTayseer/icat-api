import json

from custom_auth.models import User
from django.db import models
from rest_framework import serializers

from apps.dal.models import Assessment
from apps.dal.models.enums.ai_roles import AIRole
from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dal.models.enums.leaderboard_type import LeaderboardType
from apps.dal.models.leaderboard import Leaderboard, LeaderboardEntry
from apps.dal.models.module import Module
from apps.dal.models.user_assessment import (EssayAnswerSubmission,
                                             McqAnswerSubmission,
                                             UserAssessments)
from apps.dashboard.rest.serializers.answer import AnswerInputSerializer
from common.clients.chroma_client import ChromaClient
from common.clients.gemini_client import GeminiClient, GeminiMessage
from common.prompts import Prompts


class SubmissionSerializer(serializers.Serializer):
    assessment = serializers.PrimaryKeyRelatedField(queryset=Assessment.objects.all(), required=True)
    answers = AnswerInputSerializer(required=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    def __get_system_prompt(self, assessment_type):
        if assessment_type == AssessmentType.INITIAL:
            return Prompts.INITIAL_ASSESSMENT
        elif assessment_type == AssessmentType.MODULE:
            return Prompts.MODULE_ASSESSMENT
        return Prompts.FALLBACK_PROMPT

    def __get_context_hits(self, answers):
        chroma_client = ChromaClient()
        for answer in answers.get("mcq"):
            question = answer.get('question').get('text')
            ctx_hits = chroma_client.search_documents(question)
            answer["context"] = []
            for ctx_hit in Module.objects.filter(id__in=ctx_hits):
                answer["context"].append(ctx_hit.text)

        for answer in answers.get("essay"):
            question = answer.get('question').get('text')
            ctx_hits = chroma_client.search_documents(question)
            answer["context"] = []
            for ctx_hit in Module.objects.filter(id__in=ctx_hits):
                answer["context"].append(ctx_hit.text)

        return answers

    def __build_assessment_payload(self, assessment_type, answers):
        system_prompt = self.__get_system_prompt(assessment_type)
        if assessment_type == AssessmentType.MODULE:
            answers = self.__get_context_hits(answers)
        user_content = json.dumps(answers, indent=4)
        user_message = GeminiMessage(role=AIRole.USER, content=user_content)
        system_message = GeminiMessage(role=AIRole.SYSTEM, content=system_prompt)
        return system_message, user_message

    def __grade_with_ai(self, assessment_type, answers):
        gemini_client = GeminiClient()
        system_message, user_message = self.__build_assessment_payload(assessment_type, answers)
        response = gemini_client.chat(system_message, user_message)
        return response

    def __calculate_score_with_ai(self, assessment_type, answers):
        response = self.__grade_with_ai(assessment_type, answers)
        return response

    def __calculate_mcq_total_score(self, mcq_answers):
        total_score = 0
        for mcq in mcq_answers:
            if mcq.get("user_answer").get("id") == mcq.get("correct_choice").get("id"):
                total_score += 1
        return total_score

    def __validate_data(self, data):
        assessment = data.get('assessment')
        submitted_mcqs = data.get('answers').get('mcq', [])
        submitted_essays = data.get('answers').get('essay', [])

        submitted_mcq_question_ids = {answer.get('question').id for answer in submitted_mcqs}
        submitted_essay_question_ids = {answer.get('question').id for answer in submitted_essays}

        actual_mcq_question_ids = set(assessment.mcq_questions.values_list('id', flat=True))
        actual_essay_question_ids = set(assessment.essay_questions.values_list('id', flat=True))

        if submitted_mcq_question_ids != actual_mcq_question_ids:
            raise serializers.ValidationError({"error": "Invalid Submission."})

        if submitted_essay_question_ids != actual_essay_question_ids:
            raise serializers.ValidationError({"error": "Invalid Submission."})

        for mcq in submitted_mcqs:
            question = mcq.get('question')
            answer = mcq.get('answer')
            if answer.question != question:
                raise serializers.ValidationError({"error": "Invalid Submission."})

        return data

    def __format_answer_for_ai(self, obj):
        return {
            "id": obj.id,
            "text": obj.text
        }

    def __format_question_for_ai(self, obj):
        return {
            "id": obj.id,
            "text": obj.text,
            "max_score": obj.max_score
        }

    def __add_all_answers_to_mcq_question(self, mcq):
        mcq["user_answer"] = self.__format_answer_for_ai(mcq.get('answer'))
        mcq.pop('answer')
        mcq["answers"] = []
        for answer in mcq.get('question').answers.all():
            if answer.is_correct:
                mcq["correct_choice"] = self.__format_answer_for_ai(answer)
            else:
                mcq["answers"].append(self.__format_answer_for_ai(answer))

        return mcq

    def __add_rubric_to_essay_question(self, essay):
        essay["rubric"] = []
        for rubric in essay.get('question').rubric.all():
            essay["rubric"].append({
                "point": rubric.text,
                "weight": rubric.weight
            })

        return essay

    def __format_data_for_ai(self, validated_data):
        submitted_mcqs = validated_data.get('answers').get('mcq')
        submitted_essays = validated_data.get('answers').get('essay')
        max_score = 0

        formatted_mcqs = []
        for mcq in submitted_mcqs:
            max_score += mcq.get('question').max_score
            formatted_mcqs.append(self.__add_all_answers_to_mcq_question(mcq))
            mcq['question'] = self.__format_question_for_ai(mcq.get('question'))

        formatted_essays = []
        for essay in submitted_essays:
            max_score += essay.get('question').max_score
            formatted_essays.append(self.__add_rubric_to_essay_question(essay))
            essay['question'] = self.__format_question_for_ai(essay.get('question'))

        validated_data['answers'] = {
            "mcq": formatted_mcqs,
            "essay": formatted_essays
        }
        validated_data['max_score'] = max_score
        return validated_data

    def __find_score_and_explanation_by_id(self, question_id, response):
        for score in response.get('scores', []):
            if score.get('id') == question_id:
                return score.get('score', 0), score.get('explanation', "No explanation found")
        return 0, "No explanation found"

    def __update_user_leaderboard_entry(self, user, score):
        leaderboard_entry, _ = LeaderboardEntry.objects.get_or_create(
            user=user,
            leaderboard=Leaderboard.objects.get_or_create(type=LeaderboardType.GLOBAL)[0]
        )
        leaderboard_entry.total_score += score
        leaderboard_entry.save()

    def validate(self, data):
        validated_data = self.__validate_data(data)
        return self.__format_data_for_ai(validated_data)

    def create(self, validated_data):
        user = validated_data.get('user')
        answers = validated_data.get('answers')
        assessment = validated_data.get('assessment')
        response = self.__calculate_score_with_ai(assessment.type, answers)
        essay_user_score = response.get('overall').get('essay_total_score')
        mcq_user_score = self.__calculate_mcq_total_score(answers.get('mcq'))

        total_user_score = essay_user_score + mcq_user_score
        max_score = validated_data.get('max_score')
        feedback = response.get('overall').get('feedback')

        user_assessment = UserAssessments.objects.create(
            user=user,
            assessment=assessment,
            score=total_user_score,
            max_score=max_score,
            feedback=feedback
        )

        for mcq in answers.get('mcq'):
            _ , explanation = self.__find_score_and_explanation_by_id(mcq.get('question').get('id'), response)
            score = 1 if mcq.get("user_answer").get("id") == mcq.get("correct_choice").get("id") else 0
            McqAnswerSubmission.objects.create(
                user_assessment=user_assessment,
                question_id=mcq.get('question').get('id'),
                answer_id=mcq.get('user_answer').get('id'),
                max_score=mcq.get('question').get('max_score'),
                feedback=explanation,
                score=score
            )
        for essay in answers.get('essay'):
            score, explanation = self.__find_score_and_explanation_by_id(essay.get('question').get('id'), response)
            EssayAnswerSubmission.objects.create(
                user_assessment=user_assessment,
                question_id=essay.get('question').get('id'),
                answer=essay.get('answer'),
                max_score=essay.get('question').get('max_score'),
                feedback=explanation,
                score=score
            )

        previous_best_score = UserAssessments.objects.filter(
            user=user,
            assessment=assessment
        ).exclude(
            id=user_assessment.id
        ).aggregate(
            max_user_score=models.Max('score')
        )['max_user_score']

        # Update leaderboard if this is the first attempt or a new high score
        if previous_best_score is None or total_user_score > previous_best_score:
            self.__update_user_leaderboard_entry(user, total_user_score)
        return user_assessment


class McqAnswerSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqAnswerSubmission
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at']


class EssayAnswerSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayAnswerSubmission
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserAssessmentSerializer(serializers.ModelSerializer):
    percentage = serializers.ReadOnlyField()
    is_passed = serializers.ReadOnlyField()
    answers = serializers.SerializerMethodField()

    def get_answers(self, obj):
        return {
            "mcq": McqAnswerSubmissionSerializer(obj.mcq_answers.all(), many=True).data,
            "essay": EssayAnswerSubmissionSerializer(obj.essay_answers.all(), many=True).data
        }

    class Meta:
        model = UserAssessments
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at']
