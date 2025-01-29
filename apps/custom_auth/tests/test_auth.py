from django.contrib.auth import get_user_model
from rest_framework import status

from apps.custom_auth.tests.base import CustomAuthBaseTestCase

User = get_user_model()


class AuthTestCases(CustomAuthBaseTestCase):
    def setUp(self):
        super().setUp()

    def test_signup(self):
        data = {
            "email": "newuser@asu.com",
            "password1": "KylianMbappe7",
            "password2": "KylianMbappe7",
            "first_name": "Mazen",
            "last_name": "Tayseer",
        }
        response = self.send_unauth_request("post", f"{self.custom_auth_url}/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User registered successfully!")

    def test_duplicate_email_signup(self):
        data = {
            "email": self.user.email,
            "password1": "KylianMbappe7",
            "password2": "KylianMbappe7",
            "first_name": "Mazen",
            "last_name": "Tayseer",
        }
        response = self.send_unauth_request("post", f"{self.custom_auth_url}/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signin(self):
        data = {"email": self.user.email, "password": "Test1234"}
        response = self.send_unauth_request("post", f"{self.custom_auth_url}/signin/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_signin_invalid_credentials(self):
        data = {"email": self.user.email, "password": "WrongPassword"}
        response = self.send_unauth_request("post", f"{self.custom_auth_url}/signin/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token(self):
        self.client.cookies["refreshToken"] = self.refresh_token
        response = self.send_auth_request("post", f"{self.custom_auth_url}/token/refresh/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Token refreshed successfully")

    def test_user_info(self):
        response = self.send_auth_request("get", f"{self.custom_auth_url}/users/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)

    def test_logout(self):
        response = self.send_auth_request("post", f"{self.custom_auth_url}/logout/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logout successful.")

        self.assertEqual(response.cookies.get("token").value, "")
        self.assertEqual(response.cookies.get("refreshToken").value, "")
