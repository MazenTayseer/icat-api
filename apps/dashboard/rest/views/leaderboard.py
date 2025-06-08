from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dal.models import Leaderboard
from apps.dashboard.rest.serializers.leaderboard import LeaderboardSerializer


class LeaderboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        leaderboard = Leaderboard.objects.all().order_by('-score')
        serializer = LeaderboardSerializer(leaderboard, many=True)
        return Response(serializer.data)
