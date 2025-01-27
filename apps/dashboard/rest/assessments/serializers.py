# serializers.py
from rest_framework import serializers

from apps.dal.models import Answer, Assessment, Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class AssessmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = ['id', 'name', 'max_score', 'module', 'questions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class AssessmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['id', 'name', 'max_score', 'module', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
