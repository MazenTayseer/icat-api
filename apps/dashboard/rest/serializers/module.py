from rest_framework import serializers

from apps.dal.models import Module


class ModuleDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
