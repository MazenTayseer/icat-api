from rest_framework import serializers

from apps.dal.models import BaseAnswer, EssayAnswerRubric, McqAnswer
from apps.dal.models.question import EssayQuestion, McqQuestion


class BaseAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseAnswer
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class McqAnswerSerializer(BaseAnswerSerializer):
    class Meta(BaseAnswerSerializer.Meta):
        model = McqAnswer


class EssayAnswerRubricSerializer(BaseAnswerSerializer):
    class Meta(BaseAnswerSerializer.Meta):
        model = EssayAnswerRubric


class McqAnswerInputSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=McqQuestion.objects.all())
    answer = serializers.PrimaryKeyRelatedField(queryset=McqAnswer.objects.all())

class EssayAnswerInputSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=EssayQuestion.objects.all())
    answer = serializers.CharField()

class AnswerInputSerializer(serializers.Serializer):
    mcq = McqAnswerInputSerializer(many=True)
    essay = EssayAnswerInputSerializer(many=True)
