from rest_framework import serializers

from apps.custom_auth.models import User
from apps.dal.models import Assessment
from apps.dal.models.assessment import UserAssessments
from apps.dashboard.rest.serializers.answer import AnswerInputSerializer


class SubmissionSerializer(serializers.Serializer):
    assessment = serializers.PrimaryKeyRelatedField(queryset=Assessment.objects.all(), required=True)
    answers = AnswerInputSerializer(required=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)


    def validate(self, data):
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

    def create(self, validated_data):
        user = validated_data.get('user')
        assessment = validated_data.get('assessment')
        submitted_mcqs = validated_data.get('answers').get('mcq')
        submitted_essays = validated_data.get('answers').get('essay')

        score = self.__calculate_score(assessment, submitted_mcqs, submitted_essays)

        user_assessment = UserAssessments.objects.create(
            user=user,
            assessment=assessment,
            score=score
        )
        return user_assessment

# class AssessmentSubmissionSerializer(serializers.Serializer):
    # def validate(self, data):
    #     assessment_id = self.context["assessment_id"]
    #     try:
    #         data['assessment'] = Assessment.objects.get(id=assessment_id)
    #     except Assessment.DoesNotExist:
    #         raise serializers.ValidationError({"assessment": "Invalid assessment ID."})

    #     question_ids = [answer.get('question_id') for answer in data['answers']]
    #     valid_questions = Question.objects.filter(assessment=data['assessment'], id__in=question_ids)

    #     if len(valid_questions) != len(question_ids):
    #         raise serializers.ValidationError({"answers": "Invalid questions or questions do not belong to this assessment."})

    #     answer_ids = [answer.get('answer_id') for answer in data['answers']]
    #     valid_answers = Answer.objects.filter(question_id__in=question_ids, id__in=answer_ids)

    #     if len(valid_answers) != len(answer_ids):
    #         raise serializers.ValidationError({"answers": "Invalid answers or answers do not belong to these questions."})

    #     return data

    # def calculate_score(self, assessment, submitted_answers):
    #     correct_answers = Answer.objects.filter(
    #         question__assessment=assessment,
    #         is_correct=True
    #     )
    #     correct_answer_map = {answer.question_id: answer.id for answer in correct_answers}

    #     score = 0
    #     for answer in submitted_answers:
    #         if correct_answer_map.get(answer['question_id']) == answer['answer_id']:
    #             score += 1

    #     return score

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     assessment = validated_data['assessment']
    #     answers = validated_data['answers']

    #     score = self.calculate_score(assessment, answers)

    #     user_assessment = UserAssessments.objects.create(
    #         user=user,
    #         assessment=assessment,
    #         score=score
    #     )
    #     return user_assessment
