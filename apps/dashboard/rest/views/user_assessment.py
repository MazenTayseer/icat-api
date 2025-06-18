from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dal.models import Assessment
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
