from rest_framework import serializers

from apps.dal.models import Leaderboard
from apps.dal.models.leaderboard import LeaderboardEntry


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaderboardEntry
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    def get_users(self, obj):
        return LeaderboardEntrySerializer(obj.entries.all().order_by('-total_score'), many=True).data

    class Meta:
        model = Leaderboard
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
