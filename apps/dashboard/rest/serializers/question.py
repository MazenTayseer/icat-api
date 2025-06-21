from rest_framework import serializers

from apps.dal.models import EssayQuestion, McqQuestion
from apps.dashboard.rest.serializers.answer import (
    EssayAnswerRubricSerializer, McqAnswerSerializer)


class BaseQuestionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        if isinstance(obj, McqQuestion):
            return "mcq"
        elif isinstance(obj, EssayQuestion):
            return "essay"
        return "unknown"

    class Meta:
        abstract = True


class QuestionSerializer(serializers.Serializer):
    """Serializer that can handle both MCQ and Essay questions"""
    
    def to_representation(self, instance):
        if isinstance(instance, McqQuestion):
            return McqQuestionSerializer(instance, context=self.context).data
        elif isinstance(instance, EssayQuestion):
            return EssayQuestionSerializer(instance, context=self.context).data
        return super().to_representation(instance)


class McqQuestionSerializer(BaseQuestionSerializer):
    answers = serializers.SerializerMethodField()

    def get_answers(self, obj):
        return McqAnswerSerializer(obj.answers.all(), many=True, context=self.context).data

    def to_representation(self, instance):
        return serializers.ModelSerializer.to_representation(self, instance)

    class Meta(BaseQuestionSerializer.Meta):
        model = McqQuestion
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EssayQuestionSerializer(BaseQuestionSerializer):
    rubric = serializers.SerializerMethodField()

    def get_rubric(self, obj):
        return EssayAnswerRubricSerializer(obj.rubric.all(), many=True, context=self.context).data

    def to_representation(self, instance):
        return serializers.ModelSerializer.to_representation(self, instance)

    class Meta(BaseQuestionSerializer.Meta):
        model = EssayQuestion
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class McqQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqQuestion
        fields = ['assessment', 'domain', 'difficulty', 'text']
        
    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Question text cannot be empty")
        return value.strip()
    
    def validate_difficulty(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Difficulty must be between 1 and 5")
        return value


class EssayQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayQuestion
        fields = ['assessment', 'domain', 'difficulty', 'text']
        
    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Question text cannot be empty")
        return value.strip()
    
    def validate_difficulty(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Difficulty must be between 1 and 5")
        return value


class McqQuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqQuestion
        fields = ['assessment', 'domain', 'difficulty', 'text']
        
    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Question text cannot be empty")
        return value.strip()
    
    def validate_difficulty(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Difficulty must be between 1 and 5")
        return value


class EssayQuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayQuestion
        fields = ['assessment', 'domain', 'difficulty', 'text']
        
    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Question text cannot be empty")
        return value.strip()
    
    def validate_difficulty(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Difficulty must be between 1 and 5")
        return value
