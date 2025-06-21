from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dal.models.leaderboard import Leaderboard
from apps.dashboard.rest.serializers.leaderboard import LeaderboardSerializer


class LeaderboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        leaderboard = Leaderboard.objects.all()
        serializer = LeaderboardSerializer(leaderboard, many=True)
        return Response(serializer.data)


class LeaderboardDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, type, *args, **kwargs):
        try:
            leaderboard = Leaderboard.objects.get(type=type)
        except Leaderboard.DoesNotExist:
            return Response({"detail": "Leaderboard not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LeaderboardSerializer(leaderboard)
        return Response(serializer.data)
