from rest_framework import serializers

from apps.dal.models import EssayAnswerRubric, McqAnswer
from apps.dal.models.question import EssayQuestion, McqQuestion


class McqAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqAnswer
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EssayAnswerRubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayAnswerRubric
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class McqAnswerInputSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=McqQuestion.objects.all())
    answer = serializers.PrimaryKeyRelatedField(queryset=McqAnswer.objects.all())


class EssayAnswerInputSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=EssayQuestion.objects.all())
    answer = serializers.CharField()


class AnswerInputSerializer(serializers.Serializer):
    mcq = McqAnswerInputSerializer(many=True)
    essay = EssayAnswerInputSerializer(many=True)


class McqAnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqAnswer
        fields = ['question', 'text', 'is_correct']
        
    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Answer text cannot be empty")
        return value.strip()


class EssayAnswerRubricCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayAnswerRubric
        fields = ['question', 'text', 'weight']
        
    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Rubric text cannot be empty")
        return value.strip()
    
    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be greater than 0")
        return value


class McqAnswerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqAnswer
        fields = ['question', 'text', 'is_correct']
        
    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Answer text cannot be empty")
        return value.strip()


class EssayAnswerRubricUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayAnswerRubric
        fields = ['question', 'text', 'weight']
        
    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Rubric text cannot be empty")
        return value.strip()
    
    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be greater than 0")
        return value
