from rest_framework import serializers

from apps.dal.models import Answer, Assessment, Question, UserAssessments


class AssessmentSubmissionSerializer(serializers.Serializer):
    assessment_id = serializers.CharField()
    answers = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    trial = serializers.IntegerField()

    def validate(self, data):
        try:
            data['assessment'] = Assessment.objects.get(id=data['assessment_id'])
        except Assessment.DoesNotExist:
            raise serializers.ValidationError({"assessment_id": "Invalid assessment ID."})

        question_ids = [answer.get('question_id') for answer in data['answers']]
        valid_questions = Question.objects.filter(assessment=data['assessment'], id__in=question_ids)

        if len(valid_questions) != len(question_ids):
            raise serializers.ValidationError({"answers": "Invalid questions or questions do not belong to this assessment."})

        return data

    def calculate_score(self, assessment, submitted_answers):
        correct_answers = Answer.objects.filter(
            question__assessment=assessment,
            is_correct=True
        )
        correct_answer_map = {answer.question_id: answer.id for answer in correct_answers}

        score = 0
        for answer in submitted_answers:
            if correct_answer_map.get(answer['question_id']) == answer['answer_id']:
                score += 10
        return score

    def create(self, validated_data):
        user = self.context['request'].user
        assessment = validated_data['assessment']

        answers = validated_data['answers']

        score = self.calculate_score(assessment, answers)

        user_assessment = UserAssessments.objects.create(
            user=user,
            assessment=assessment,
            score=score
        )
        return user_assessment
