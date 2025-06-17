from custom_auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "created_at", "updated_at"]
        read_only_fields = ['id', 'created_at', 'updated_at']
