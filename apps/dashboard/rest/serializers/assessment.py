from rest_framework import serializers

from apps.dal.models import Assessment
from apps.dashboard.rest.serializers.question import BaseQuestionSerializer


class AssessmentSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    max_retries = serializers.SerializerMethodField()

    def get_questions(self, obj):
        questions_list = list(obj.questions)[:obj.max_questions_at_once]
        return BaseQuestionSerializer(questions_list, many=True, context=self.context).data

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
