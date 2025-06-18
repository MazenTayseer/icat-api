import json

from custom_auth.models import User
from rest_framework import serializers

from apps.dal.models import Assessment
from apps.dal.models.assessment import UserAssessments
from apps.dal.models.enums.ai_roles import AIRole
from apps.dashboard.rest.serializers.answer import AnswerInputSerializer
from common.clients.ollama_client import OllamaClient, OllamaMessage
from common.prompts import Prompts


class SubmissionSerializer(serializers.Serializer):
    assessment = serializers.PrimaryKeyRelatedField(queryset=Assessment.objects.all(), required=True)
    answers = AnswerInputSerializer(required=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    def __build_assessment_payload(self, answers):
        user_content = Prompts.GRADING_DIRECTIVE + json.dumps(answers, indent=4)
        user_message = OllamaMessage(role=AIRole.USER, content=user_content)
        system_message = OllamaMessage(role=AIRole.SYSTEM, content=Prompts.INITIAL_ASSESSMENT)
        return [system_message, user_message]

    def __grade_with_ai(self, answers):
        ollama_client = OllamaClient()
        payload = self.__build_assessment_payload(answers)
        response = ollama_client.chat(payload)
        return response

    def __calculate_score_with_ai(self, answers):
        response = self.__grade_with_ai(answers)
        return response

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

    def __format_object_to_id_and_text(self, obj):
        return {
            "id": obj.id,
            "text": obj.text
        }

    def __add_all_answers_to_mcq_question(self, mcq):
        mcq["user_answer"] = self.__format_object_to_id_and_text(mcq.get('answer'))
        mcq.pop('answer')
        mcq["answers"] = []
        for answer in mcq.get('question').answers.all():
            if answer.is_correct:
                mcq["correct_choice"] = self.__format_object_to_id_and_text(answer)
            else:
                mcq["answers"].append(self.__format_object_to_id_and_text(answer))

        return mcq

    def __add_rubric_to_essay_question(self, essay):
        essay["rubric"] = []
        for rubric in essay.get('question').rubric.all():
            essay["rubric"].append({
                "point": rubric.text,
                "value": rubric.value,
                "weight": rubric.weight
            })

        return essay

    def __format_data_for_ai(self, validated_data):
        submitted_mcqs = validated_data.get('answers').get('mcq')
        submitted_essays = validated_data.get('answers').get('essay')

        formatted_mcqs = []
        for mcq in submitted_mcqs:
            formatted_mcqs.append(self.__add_all_answers_to_mcq_question(mcq))
            mcq['question'] = self.__format_object_to_id_and_text(mcq.get('question'))

        formatted_essays = []
        for essay in submitted_essays:
            formatted_essays.append(self.__add_rubric_to_essay_question(essay))
            essay['question'] = self.__format_object_to_id_and_text(essay.get('question'))

        validated_data['answers'] = {
            "mcq": formatted_mcqs,
            "essay": formatted_essays
        }
        return validated_data

    def validate(self, data):
        validated_data = self.__validate_data(data)
        return self.__format_data_for_ai(validated_data)

    def create(self, validated_data):
        user = validated_data.get('user')
        answers = validated_data.get('answers')
        assessment = validated_data.get('assessment')
        response = self.__calculate_score_with_ai(answers)

        user_assessment = UserAssessments.objects.create(
            user=user,
            assessment=assessment,
            score=response.get('overall').get('score'),
            feedback=response.get('overall').get('feedback')
        )
        return user_assessment



class UserAssessmentSerializer(serializers.ModelSerializer):
    score_percentage = serializers.ReadOnlyField()
    is_passed = serializers.ReadOnlyField()

    class Meta:
        model = UserAssessments
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at']
