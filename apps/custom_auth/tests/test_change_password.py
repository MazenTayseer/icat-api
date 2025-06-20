from custom_auth.tests.base import CustomAuthBaseTestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class ChangePasswordTestCases(CustomAuthBaseTestCase):
    def setUp(self):
        super().setUp()

    def test_change_password_success(self):
        data = {
            "current_password": "Test1234",
            "new_password_1": "NewPassword123",
            "new_password2": "NewPassword123",
        }
        response = self.send_auth_request("post", f"{self.custom_auth_url}/change-password/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password changed successfully!")

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPassword123"))
        self.assertFalse(self.user.check_password("Test1234"))

    def test_change_password_wrong_current_password(self):
        data = {
            "current_password": "WrongPassword",
            "new_password_1": "NewPassword123",
            "new_password2": "NewPassword123",
        }
        response = self.send_auth_request("post", f"{self.custom_auth_url}/change-password/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Current password is incorrect", str(response.data))

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Test1234"))

    def test_change_password_mismatched_new_passwords(self):
        data = {
            "current_password": "Test1234",
            "new_password_1": "NewPassword123",
            "new_password2": "DifferentPassword123",
        }
        response = self.send_auth_request("post", f"{self.custom_auth_url}/change-password/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("New password fields didn't match", str(response.data))

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Test1234"))

    def test_change_password_weak_new_password(self):
        data = {
            "current_password": "Test1234",
            "new_password_1": "123",
            "new_password2": "123",
        }
        response = self.send_auth_request("post", f"{self.custom_auth_url}/change-password/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Test1234"))
