from rest_framework import serializers

from apps.dal.models import Assessment
from apps.dashboard.rest.serializers.question import BaseQuestionSerializer


class AssessmentSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    def get_questions(self, obj):
        all_questions = list(obj.questions)
        return BaseQuestionSerializer(all_questions, many=True, context=self.context).data

    class Meta:
        model = Assessment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AssessmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
