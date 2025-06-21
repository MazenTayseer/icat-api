from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.dal.models import McqQuestion, EssayQuestion
from apps.dashboard.rest.serializers.question import (
    McqQuestionSerializer, EssayQuestionSerializer,
    McqQuestionCreateSerializer, EssayQuestionCreateSerializer,
    McqQuestionUpdateSerializer, EssayQuestionUpdateSerializer
)


class McqQuestionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None, *args, **kwargs):
        if id:
            try:
                question = McqQuestion.objects.get(id=id)
            except McqQuestion.DoesNotExist:
                return Response({"detail": "MCQ Question not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = McqQuestionSerializer(question)
            return Response(serializer.data)

        questions = McqQuestion.objects.all()
        serializer = McqQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = McqQuestionCreateSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            response_serializer = McqQuestionSerializer(question)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        try:
            question = McqQuestion.objects.get(id=id)
        except McqQuestion.DoesNotExist:
            return Response({"detail": "MCQ Question not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = McqQuestionUpdateSerializer(question, data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            response_serializer = McqQuestionSerializer(question)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        try:
            question = McqQuestion.objects.get(id=id)
        except McqQuestion.DoesNotExist:
            return Response({"detail": "MCQ Question not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = McqQuestionUpdateSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            response_serializer = McqQuestionSerializer(question)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        try:
            question = McqQuestion.objects.get(id=id)
        except McqQuestion.DoesNotExist:
            return Response({"detail": "MCQ Question not found."}, status=status.HTTP_404_NOT_FOUND)

        question.delete()
        return Response({"detail": "MCQ Question deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class EssayQuestionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None, *args, **kwargs):
        if id:
            try:
                question = EssayQuestion.objects.get(id=id)
            except EssayQuestion.DoesNotExist:
                return Response({"detail": "Essay Question not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = EssayQuestionSerializer(question)
            return Response(serializer.data)

        questions = EssayQuestion.objects.all()
        serializer = EssayQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = EssayQuestionCreateSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            response_serializer = EssayQuestionSerializer(question)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        try:
            question = EssayQuestion.objects.get(id=id)
        except EssayQuestion.DoesNotExist:
            return Response({"detail": "Essay Question not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EssayQuestionUpdateSerializer(question, data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            response_serializer = EssayQuestionSerializer(question)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        try:
            question = EssayQuestion.objects.get(id=id)
        except EssayQuestion.DoesNotExist:
            return Response({"detail": "Essay Question not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EssayQuestionUpdateSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            response_serializer = EssayQuestionSerializer(question)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        try:
            question = EssayQuestion.objects.get(id=id)
        except EssayQuestion.DoesNotExist:
            return Response({"detail": "Essay Question not found."}, status=status.HTTP_404_NOT_FOUND)

        question.delete()
        return Response({"detail": "Essay Question deleted successfully."}, status=status.HTTP_204_NO_CONTENT) 