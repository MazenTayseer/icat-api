import json

from django.test import TestCase
from rest_framework.test import APIClient

from common.tests.factory.UserFactory import UserFactory


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(
            email="test@test.com",
            password="Test1234",
            is_superuser=True
        )
        self.auth_token, self.refresh_token = self._get_auth_token(self.user.email, "Test1234")

    def _get_auth_token(self, email, password):
        response = self.client.post(
            "/api/auth/signin/",
            {"email": email, "password": password},
            format="json"
        )
        return response.data.get("access"), response.data.get("refresh")

    def send_auth_request(self, method, url, data=None, **kwargs):
        """
        Helper method to send authenticated requests.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.auth_token}")
        return self.client.generic(method, url, json.dumps(data), content_type='application/json', **kwargs)

    def send_unauth_request(self, method, url, data=None, **kwargs):
        """
        Helper method to send unauthenticated requests.
        """
        self.client.credentials()
        return self.client.generic(method, url, json.dumps(data), content_type='application/json', **kwargs)
