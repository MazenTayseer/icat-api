from rest_framework import serializers

from apps.dal.models import Module


class ModuleDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class ModuleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['name', 'description', 'text']
        
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Module name cannot be empty")
        return value.strip()
    
    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Module description cannot be empty")
        return value.strip()
    
    def validate_text(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Text must be a list")
        if len(value) == 0:
            raise serializers.ValidationError("Text cannot be empty")
        return value


class ModuleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['name', 'description', 'text']
        
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Module name cannot be empty")
        return value.strip()
    
    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Module description cannot be empty")
        return value.strip()
    
    def validate_text(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Text must be a list")
        if len(value) == 0:
            raise serializers.ValidationError("Text cannot be empty")
        return value
