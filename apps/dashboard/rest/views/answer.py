from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dal.models import McqAnswer, EssayAnswerRubric
from apps.dashboard.rest.serializers.answer import (
    McqAnswerSerializer, EssayAnswerRubricSerializer,
    McqAnswerCreateSerializer, EssayAnswerRubricCreateSerializer,
    McqAnswerUpdateSerializer, EssayAnswerRubricUpdateSerializer
)


class McqAnswerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None, *args, **kwargs):
        if id:
            try:
                answer = McqAnswer.objects.get(id=id)
            except McqAnswer.DoesNotExist:
                return Response({"detail": "MCQ Answer not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = McqAnswerSerializer(answer)
            return Response(serializer.data)

        answers = McqAnswer.objects.all()
        serializer = McqAnswerSerializer(answers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = McqAnswerCreateSerializer(data=request.data)
        if serializer.is_valid():
            answer = serializer.save()
            response_serializer = McqAnswerSerializer(answer)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        try:
            answer = McqAnswer.objects.get(id=id)
        except McqAnswer.DoesNotExist:
            return Response({"detail": "MCQ Answer not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = McqAnswerUpdateSerializer(answer, data=request.data)
        if serializer.is_valid():
            answer = serializer.save()
            response_serializer = McqAnswerSerializer(answer)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        try:
            answer = McqAnswer.objects.get(id=id)
        except McqAnswer.DoesNotExist:
            return Response({"detail": "MCQ Answer not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = McqAnswerUpdateSerializer(answer, data=request.data, partial=True)
        if serializer.is_valid():
            answer = serializer.save()
            response_serializer = McqAnswerSerializer(answer)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        try:
            answer = McqAnswer.objects.get(id=id)
        except McqAnswer.DoesNotExist:
            return Response({"detail": "MCQ Answer not found."}, status=status.HTTP_404_NOT_FOUND)

        answer.delete()
        return Response({"detail": "MCQ Answer deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class EssayAnswerRubricView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None, *args, **kwargs):
        if id:
            try:
                rubric = EssayAnswerRubric.objects.get(id=id)
            except EssayAnswerRubric.DoesNotExist:
                return Response({"detail": "Essay Answer Rubric not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = EssayAnswerRubricSerializer(rubric)
            return Response(serializer.data)

        rubrics = EssayAnswerRubric.objects.all()
        serializer = EssayAnswerRubricSerializer(rubrics, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = EssayAnswerRubricCreateSerializer(data=request.data)
        if serializer.is_valid():
            rubric = serializer.save()
            response_serializer = EssayAnswerRubricSerializer(rubric)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        try:
            rubric = EssayAnswerRubric.objects.get(id=id)
        except EssayAnswerRubric.DoesNotExist:
            return Response({"detail": "Essay Answer Rubric not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EssayAnswerRubricUpdateSerializer(rubric, data=request.data)
        if serializer.is_valid():
            rubric = serializer.save()
            response_serializer = EssayAnswerRubricSerializer(rubric)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        try:
            rubric = EssayAnswerRubric.objects.get(id=id)
        except EssayAnswerRubric.DoesNotExist:
            return Response({"detail": "Essay Answer Rubric not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EssayAnswerRubricUpdateSerializer(rubric, data=request.data, partial=True)
        if serializer.is_valid():
            rubric = serializer.save()
            response_serializer = EssayAnswerRubricSerializer(rubric)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        try:
            rubric = EssayAnswerRubric.objects.get(id=id)
        except EssayAnswerRubric.DoesNotExist:
            return Response({"detail": "Essay Answer Rubric not found."}, status=status.HTTP_404_NOT_FOUND)

        rubric.delete()
        return Response({"detail": "Essay Answer Rubric deleted successfully."}, status=status.HTTP_204_NO_CONTENT) 