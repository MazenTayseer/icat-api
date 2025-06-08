from rest_framework import serializers

from apps.dal.models import BaseQuestion, EssayQuestion, McqQuestion
from apps.dashboard.rest.serializers.answer import (
    EssayAnswerRubricSerializer, McqAnswerSerializer)


class BaseQuestionSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        if isinstance(instance, McqQuestion):
            data = McqQuestionSerializer(instance, context=self.context).data
            data['type'] = 'mcq'
        elif isinstance(instance, EssayQuestion):
            data = EssayQuestionSerializer(instance, context=self.context).data
            data['type'] = 'essay'
        return data

    class Meta:
        model = BaseQuestion
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class McqQuestionSerializer(BaseQuestionSerializer):
    answers = serializers.SerializerMethodField()

    def get_answers(self, obj):
        return McqAnswerSerializer(obj.answers.all(), many=True, context=self.context).data

    def to_representation(self, instance):
        return serializers.ModelSerializer.to_representation(self, instance)

    class Meta(BaseQuestionSerializer.Meta):
        model = McqQuestion


class EssayQuestionSerializer(BaseQuestionSerializer):
    rubric = serializers.SerializerMethodField()

    def get_rubric(self, obj):
        return EssayAnswerRubricSerializer(obj.rubric.all(), many=True, context=self.context).data

    def to_representation(self, instance):
        return serializers.ModelSerializer.to_representation(self, instance)

    class Meta(BaseQuestionSerializer.Meta):
        model = EssayQuestion
