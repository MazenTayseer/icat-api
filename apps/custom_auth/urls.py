from custom_auth.rest.views import (ChangePasswordView, RefreshTokenView,
                                    SignInView, SignUpView, UserView)
from django.urls import path

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('users/me/', UserView.as_view(), name='user_me'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
