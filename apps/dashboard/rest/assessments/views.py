# views.py
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dal.models import Assessment
from apps.dashboard.rest.assessments.serializers import (
    AssessmentListSerializer, AssessmentSerializer)


class AssessmentDashboardListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        module_id = request.query_params.get("module_id", None)

        if module_id:
            assessments = Assessment.objects.filter(module_id=module_id)
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

        serializer = AssessmentSerializer(assessment)
        return Response(serializer.data)
