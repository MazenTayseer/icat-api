
from apps.dashboard.tests.base import DashboardBaseTestCase
from apps.dashboard.tests.factory import ModuleFactory


class ModuleTestCases(DashboardBaseTestCase):
    def setUp(self):
        self.module_1 = ModuleFactory(name='Module 1')
        self.module_2 = ModuleFactory(name='Module 2')

        super().setUp()

    def test_get_all_module(self):
        url = f"{self.dashboard_url}/modules/"
        response = self.send_auth_request("get", url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_one_module(self):
        url = f"{self.dashboard_url}/modules/{self.module_1.id}/"
        response = self.send_auth_request("get", url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("id"), self.module_1.id)
        self.assertEqual(response.data.get("name"), 'Module 1')
