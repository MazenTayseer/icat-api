from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dashboard.tests.base import DashboardBaseTestCase
from common.tests.factory import ModuleFactory


class AssessmentCreationTestCase(DashboardBaseTestCase):
    def setUp(self):
        super().setUp()
        self.module = ModuleFactory()

    def test_create_initial_assessment_success(self):
        url = f"{self.dashboard_url}/assessments/"
        data = {
            "name": "Initial Assessment",
            "type": AssessmentType.INITIAL,
            "max_questions_at_once": 10,
            "max_retries": 1
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("name"), "Initial Assessment")
        self.assertEqual(response.data.get("type"), AssessmentType.INITIAL)
        self.assertIsNone(response.data.get("module"))
        self.assertEqual(response.data.get("max_questions_at_once"), 10)
        self.assertEqual(response.data.get("max_retries"), 1)

    def test_create_module_assessment_success(self):
        url = f"{self.dashboard_url}/assessments/"
        data = {
            "name": "Module Assessment",
            "type": AssessmentType.MODULE,
            "module": self.module.id,
            "max_questions_at_once": 5,
            "max_retries": 3
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("name"), "Module Assessment")
        self.assertEqual(response.data.get("type"), AssessmentType.MODULE)
        self.assertEqual(response.data.get("module"), self.module.id)
        self.assertEqual(response.data.get("max_questions_at_once"), 5)
        self.assertEqual(response.data.get("max_retries"), 3)

    def test_create_initial_assessment_with_module_error(self):
        url = f"{self.dashboard_url}/assessments/"
        data = {
            "name": "Initial Assessment",
            "type": AssessmentType.INITIAL,
            "module": self.module.id,
            "max_questions_at_once": 10,
            "max_retries": 1
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)

    def test_create_module_assessment_without_module_error(self):
        url = f"{self.dashboard_url}/assessments/"
        data = {
            "name": "Module Assessment",
            "type": AssessmentType.MODULE,
            "max_questions_at_once": 5,
            "max_retries": 3
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)

    def test_create_assessment_empty_name(self):
        url = f"{self.dashboard_url}/assessments/"
        data = {
            "name": "",
            "type": AssessmentType.INITIAL,
            "max_questions_at_once": 10,
            "max_retries": 1
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.data) 