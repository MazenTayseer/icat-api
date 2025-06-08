from rest_framework import serializers

from apps.dal.models import Leaderboard


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
