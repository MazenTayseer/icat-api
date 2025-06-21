from rest_framework import serializers

from apps.dal.models import Assessment
from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dashboard.rest.serializers.question import QuestionSerializer


class AssessmentSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    max_retries = serializers.SerializerMethodField()

    def get_questions(self, obj):
        questions_list = list(obj.questions)[:obj.max_questions_at_once]
        return QuestionSerializer(questions_list, many=True, context=self.context).data

    def get_max_retries(self, obj):
        return obj.max_retries

    class Meta:
        model = Assessment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AssessmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AssessmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['name', 'type', 'module', 'max_questions_at_once', 'max_retries']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Assessment name cannot be empty")
        return value.strip()

    def validate(self, data):
        assessment_type = data.get('type')
        module = data.get('module')

        if assessment_type == AssessmentType.INITIAL and module:
            raise serializers.ValidationError("Initial assessment cannot have a module")

        if assessment_type == AssessmentType.MODULE and not module:
            raise serializers.ValidationError("Module assessment must have a module")

        return data


class AssessmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['name', 'type', 'module', 'max_questions_at_once', 'max_retries']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Assessment name cannot be empty")
        return value.strip()

    def validate(self, data):
        assessment_type = data.get('type')
        module = data.get('module')

        if assessment_type == AssessmentType.INITIAL and module:
            raise serializers.ValidationError("Initial assessment cannot have a module")

        if assessment_type == AssessmentType.MODULE and not module:
            raise serializers.ValidationError("Module assessment must have a module")

        return data
