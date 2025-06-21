from apps.dashboard.tests.base import DashboardBaseTestCase
from common.tests.factory import ModuleFactory


class ModuleUpdateDeleteTestCase(DashboardBaseTestCase):
    def setUp(self):
        super().setUp()
        self.module = ModuleFactory(
            name="Original Module",
            description="Original description",
            text=["Original section 1", "Original section 2"]
        )

    def test_update_module_success(self):
        url = f"{self.dashboard_url}/modules/{self.module.id}/"
        data = {
            "name": "Updated Module",
            "description": "Updated description",
            "text": ["Updated section 1", "Updated section 2", "New section 3"]
        }
        response = self.send_auth_request("put", url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("name"), "Updated Module")
        self.assertEqual(response.data.get("description"), "Updated description")
        self.assertEqual(len(response.data.get("text")), 3)
        self.assertEqual(response.data.get("text")[2], "New section 3")

    def test_partial_update_module_success(self):
        url = f"{self.dashboard_url}/modules/{self.module.id}/"
        data = {
            "name": "Partially Updated Module"
        }
        response = self.send_auth_request("patch", url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("name"), "Partially Updated Module")
        self.assertEqual(response.data.get("description"), "Original description")
        self.assertEqual(len(response.data.get("text")), 2)

    def test_update_module_empty_name(self):
        url = f"{self.dashboard_url}/modules/{self.module.id}/"
        data = {
            "name": "",
            "description": "Updated description",
            "text": ["Updated section 1"]
        }
        response = self.send_auth_request("put", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.data)

    def test_update_module_empty_text(self):
        url = f"{self.dashboard_url}/modules/{self.module.id}/"
        data = {
            "name": "Updated Module",
            "description": "Updated description",
            "text": []
        }
        response = self.send_auth_request("put", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("text", response.data)

    def test_update_module_not_found(self):
        url = f"{self.dashboard_url}/modules/non-existent-id/"
        data = {
            "name": "Updated Module",
            "description": "Updated description",
            "text": ["Updated section 1"]
        }
        response = self.send_auth_request("put", url, data=data)

        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.data.get("detail").lower())

    def test_delete_module_success(self):
        url = f"{self.dashboard_url}/modules/{self.module.id}/"
        response = self.send_auth_request("delete", url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data.get("detail"), "Module deleted successfully.")

    def test_delete_module_not_found(self):
        url = f"{self.dashboard_url}/modules/non-existent-id/"
        response = self.send_auth_request("delete", url)

        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.data.get("detail").lower()) 