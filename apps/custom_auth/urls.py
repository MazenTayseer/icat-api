from django.urls import path

from apps.custom_auth.rest.views import SignUpView

urlpatterns = [
    path('signup', SignUpView().as_view(), name='signup'),
]
