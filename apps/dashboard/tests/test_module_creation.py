from apps.dashboard.tests.base import DashboardBaseTestCase


class ModuleCreationTestCase(DashboardBaseTestCase):
    def setUp(self):
        super().setUp()

    def test_create_module_success(self):
        url = f"{self.dashboard_url}/modules/"
        data = {
            "name": "Test Module",
            "description": "This is a test module for cybersecurity awareness",
            "text": [
                "Section 1: Introduction to Cybersecurity",
                "Section 2: Common Threats",
                "Section 3: Best Practices"
            ]
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("name"), "Test Module")
        self.assertEqual(response.data.get("description"), "This is a test module for cybersecurity awareness")
        self.assertEqual(len(response.data.get("text")), 3)
        self.assertIsNotNone(response.data.get("id"))

    def test_create_module_empty_name(self):
        url = f"{self.dashboard_url}/modules/"
        data = {
            "name": "",
            "description": "This is a test module",
            "text": ["Section 1"]
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.data)

    def test_create_module_empty_description(self):
        url = f"{self.dashboard_url}/modules/"
        data = {
            "name": "Test Module",
            "description": "",
            "text": ["Section 1"]
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("description", response.data)

    def test_create_module_empty_text(self):
        url = f"{self.dashboard_url}/modules/"
        data = {
            "name": "Test Module",
            "description": "This is a test module",
            "text": []
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("text", response.data)

    def test_create_module_invalid_text_type(self):
        url = f"{self.dashboard_url}/modules/"
        data = {
            "name": "Test Module",
            "description": "This is a test module",
            "text": "This should be a list"
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("text", response.data) 