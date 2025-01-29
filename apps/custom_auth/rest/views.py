from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
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
                key='refreshToken',
                value=refresh_token,
                samesite='Lax',
                max_age=settings.REFRESH_TOKEN_LIFETIME,
            )
            response.set_cookie(
                key='token',
                value=access_token,
                samesite='Lax',
                max_age=settings.ACCESS_TOKEN_LIFETIME,
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refreshToken')
        if not refresh_token:
            return Response(
                {"error": "Refresh token not provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({
                'message': 'Token refreshed successfully',
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='token',
                value=access_token,
                httponly=True,
                samesite='Lax',
                max_age=settings.ACCESS_TOKEN_LIFETIME,
            )
            return response
        except TokenError as e:
            raise InvalidToken(e.args[0])


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {
            'id': user.id,
            'experience_level': user.experience_level,
            'username': user.username,
            'email': user.email,
        }
        return Response(data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(
            {"message": "Logout successful."},
            status=status.HTTP_200_OK
        )
        response.delete_cookie('token')
        response.delete_cookie('refreshToken')
        return response
