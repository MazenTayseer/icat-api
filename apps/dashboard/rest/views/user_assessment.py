from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dashboard.rest.serializers.user_assessment import \
    SubmissionSerializer


class AssessmentSubmissionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, assessment_id, *args, **kwargs):
        answers = request.data.get('answers')
        data = {
            "answers": answers,
            "assessment": assessment_id,
            "user": request.user
        }
        serializer = SubmissionSerializer(data=data)
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
