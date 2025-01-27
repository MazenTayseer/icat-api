from django.urls import path

from apps.custom_auth.rest.views import (RefreshTokenView, SignInView,
                                         SignUpView)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]
