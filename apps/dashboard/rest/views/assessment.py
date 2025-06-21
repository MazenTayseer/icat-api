from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dal.models import Assessment, UserAssessments
from apps.dashboard.rest.serializers.assessment import (
    AssessmentListSerializer, AssessmentSerializer)


class AssessmentDashboardListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        module = request.query_params.get("module", None)
        type = request.query_params.get("type", None)

        if module:
            assessments = Assessment.objects.filter(module_id=module)
        elif type:
            assessments = Assessment.objects.filter(type__iexact=type)
        else:
            assessments = Assessment.objects.all()

        serializer = AssessmentListSerializer(assessments, many=True)
        return Response(serializer.data)

class AssessmentDashboardDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        try:
            assessment = Assessment.objects.get(id=id)
        except Assessment.DoesNotExist:
            return Response({"detail": "Assessment not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        user_assessment = UserAssessments.objects.filter(user=user, assessment=assessment).count()
        if user_assessment >= assessment.max_retries:
            return Response({"detail": "You have reached the maximum number of retries."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AssessmentSerializer(assessment)
        return Response(serializer.data)
