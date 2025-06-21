from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dal.models import Assessment
from apps.dal.models.user_assessment import UserAssessments
from apps.dashboard.rest.serializers.user_assessment import (
    SubmissionSerializer, UserAssessmentSerializer)


class AssessmentSubmissionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, assessment_id, *args, **kwargs):
        try:
            assessment = Assessment.objects.get(id=assessment_id)
        except Assessment.DoesNotExist:
            return Response({"detail": "Assessment not found."}, status=status.HTTP_404_NOT_FOUND)

        answers = request.data.get('answers')
        data = {
            "answers": answers,
            "assessment": assessment.id,
            "user": request.user.id
        }
        serializer = SubmissionSerializer(data=data)
        if serializer.is_valid():
            user_assessment = serializer.save()
            user_assessment_serializer = UserAssessmentSerializer(user_assessment)
            return Response(user_assessment_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAssessmentListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, assessment_id, *args, **kwargs):
        try:
            assessment = Assessment.objects.get(id=assessment_id)
        except Assessment.DoesNotExist:
            return Response({"detail": "Assessment not found."}, status=status.HTTP_404_NOT_FOUND)

        user_assessments = UserAssessments.objects.filter(
            user=request.user,
            assessment=assessment
        ).order_by('-created_at')

        serializer = UserAssessmentSerializer(user_assessments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAssessmentDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, submission_id, *args, **kwargs):
        try:
            user_assessment = UserAssessments.objects.get(id=submission_id)
        except UserAssessments.DoesNotExist:
            return Response({"detail": "Submission not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserAssessmentSerializer(user_assessment)
        return Response(serializer.data, status=status.HTTP_200_OK)
