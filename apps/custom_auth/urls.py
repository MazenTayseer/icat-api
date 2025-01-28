from django.urls import path

from apps.custom_auth.rest.views import (LogoutView, RefreshTokenView,
                                         SignInView, SignUpView, UserView)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('users/me/', UserView.as_view(), name='user_me'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
