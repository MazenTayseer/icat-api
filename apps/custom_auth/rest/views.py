from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.custom_auth.rest.serializers import (SignInSerializer,
                                               SignUpSerializer)


class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED
            )
        else:
            print("Serializer errors:", serializer.errors)

            return Response(
                {"errors": serializer.errors},  # JSON with error details
                status=status.HTTP_400_BAD_REQUEST
            )




class SignInView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({
                'message': 'Login successful',
                'access': access_token,
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                max_age=settings.REFRESH_TOKEN_LIFETIME,
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {"error": "Refresh token not provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token}, status=status.HTTP_200_OK)
        except TokenError as e:
            raise InvalidToken(e.args[0])
