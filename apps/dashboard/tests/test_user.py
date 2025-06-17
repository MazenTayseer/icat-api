
from apps.dashboard.tests.base import DashboardBaseTestCase


class UserTestCases(DashboardBaseTestCase):
    def setUp(self):
        super().setUp()

    def test_get_user(self):
        url = f"{self.dashboard_url}/user/"
        response = self.send_auth_request("get", url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("id"), self.user.id)
        self.assertEqual(response.data.get("first_name"), self.user.first_name)
        self.assertEqual(response.data.get("last_name"), self.user.last_name)
        self.assertEqual(response.data.get("email"), self.user.email)
