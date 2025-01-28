from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dashboard.rest.user_assessment.serializers import \
    AssessmentSubmissionSerializer


class AssessmentSubmissionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, assessment_id, *args, **kwargs):
        serializer = AssessmentSubmissionSerializer(
            data=request.data,
            context={
                "request": request,
                "assessment_id": assessment_id
            }
        )
        if serializer.is_valid():
            user_assessment = serializer.save()
            return Response(
                {
                    "message": "Submission successful",
                    "score": user_assessment.score,
                    "score_percentage": user_assessment.score_percentage,
                    "is_passed": user_assessment.is_passed
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
