from rest_framework import serializers

from apps.dal.models import Leaderboard
from apps.dal.models.leaderboard import LeaderboardEntry


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    modules_completed = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    def get_modules_completed(self, obj):
        return obj.modules_completed

    def get_position(self, obj):
        return obj.position

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

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
