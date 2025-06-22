from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dal.models import Assessment, UserAssessments
from apps.dashboard.rest.serializers.assessment import (
    AssessmentCreateSerializer, AssessmentListSerializer, AssessmentSerializer,
    AssessmentUpdateSerializer)
from common.permissions import IsSuperUserOrReadOnly


class AssessmentDashboardListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUserOrReadOnly]

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

    def post(self, request, *args, **kwargs):
        serializer = AssessmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            assessment = serializer.save()
            response_serializer = AssessmentListSerializer(assessment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssessmentDashboardDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUserOrReadOnly]

    def get(self, request, id, *args, **kwargs):
        try:
            assessment = Assessment.objects.get(id=id)
        except Assessment.DoesNotExist:
            return Response({"detail": "Assessment not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        user_assessment_count = UserAssessments.objects.filter(user=user, assessment=assessment).count()
        if user_assessment_count >= assessment.max_retries:
            return Response({"detail": "You have reached the maximum number of retries."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AssessmentSerializer(assessment)
        return Response(serializer.data)

    def put(self, request, id, *args, **kwargs):
        try:
            assessment = Assessment.objects.get(id=id)
        except Assessment.DoesNotExist:
            return Response({"detail": "Assessment not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AssessmentUpdateSerializer(assessment, data=request.data)
        if serializer.is_valid():
            assessment = serializer.save()
            response_serializer = AssessmentListSerializer(assessment)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        try:
            assessment = Assessment.objects.get(id=id)
        except Assessment.DoesNotExist:
            return Response({"detail": "Assessment not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AssessmentUpdateSerializer(assessment, data=request.data, partial=True)
        if serializer.is_valid():
            assessment = serializer.save()
            response_serializer = AssessmentListSerializer(assessment)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        try:
            assessment = Assessment.objects.get(id=id)
        except Assessment.DoesNotExist:
            return Response({"detail": "Assessment not found."}, status=status.HTTP_404_NOT_FOUND)

        assessment.delete()
        return Response({"detail": "Assessment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
