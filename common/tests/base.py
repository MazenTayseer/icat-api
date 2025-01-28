from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com",
            password="Test1234"
        )
        self.auth_token = self._get_auth_token(self.user.email, "Test1234")

    def _get_auth_token(self, email, password):
        response = self.client.post(
            f"{settings.BASE_URL}/api/auth/signin/",
            {"email": email, "password": password},
            format="json"
        )
        return response.data.get("access")

    def send_auth_request(self, method, url, data=None, **kwargs):
        """
        Helper method to send authenticated requests.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.auth_token}")
        return self.client.generic(method, url, data, **kwargs)

    def send_unauth_request(self, method, url, data=None, **kwargs):
        """
        Helper method to send unauthenticated requests.
        """
        self.client.credentials()
        return self.client.generic(method, url, data, **kwargs)
