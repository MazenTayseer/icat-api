from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dashboard.tests.base import DashboardBaseTestCase
from common.tests.factory import AssessmentFactory, ModuleFactory


class AssessmentUpdateDeleteTestCase(DashboardBaseTestCase):
    def setUp(self):
        super().setUp()
        self.module = ModuleFactory()
        self.initial_assessment = AssessmentFactory(
            name="Original Initial Assessment",
            type=AssessmentType.INITIAL,
            module=None,
            max_questions_at_once=5,
            max_retries=1
        )
        self.module_assessment = AssessmentFactory(
            name="Original Module Assessment",
            type=AssessmentType.MODULE,
            module=self.module,
            max_questions_at_once=3,
            max_retries=2
        )

    def test_update_initial_assessment_success(self):
        url = f"{self.dashboard_url}/assessments/{self.initial_assessment.id}/"
        data = {
            "name": "Updated Initial Assessment",
            "type": AssessmentType.INITIAL,
            "max_questions_at_once": 10,
            "max_retries": 1
        }
        response = self.send_auth_request("put", url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("name"), "Updated Initial Assessment")
        self.assertEqual(response.data.get("type"), AssessmentType.INITIAL)
        self.assertIsNone(response.data.get("module"))
        self.assertEqual(response.data.get("max_questions_at_once"), 10)

    def test_update_module_assessment_success(self):
        url = f"{self.dashboard_url}/assessments/{self.module_assessment.id}/"
        data = {
            "name": "Updated Module Assessment",
            "type": AssessmentType.MODULE,
            "module": self.module.id,
            "max_questions_at_once": 7,
            "max_retries": 3
        }
        response = self.send_auth_request("put", url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("name"), "Updated Module Assessment")
        self.assertEqual(response.data.get("type"), AssessmentType.MODULE)
        self.assertEqual(response.data.get("module"), self.module.id)
        self.assertEqual(response.data.get("max_questions_at_once"), 7)

    def test_partial_update_assessment_success(self):
        url = f"{self.dashboard_url}/assessments/{self.initial_assessment.id}/"
        data = {
            "name": "Partially Updated Assessment"
        }
        response = self.send_auth_request("patch", url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("name"), "Partially Updated Assessment")
        self.assertEqual(response.data.get("type"), AssessmentType.INITIAL)
        self.assertEqual(response.data.get("max_questions_at_once"), 5)

    def test_update_initial_assessment_with_module_error(self):
        url = f"{self.dashboard_url}/assessments/{self.initial_assessment.id}/"
        data = {
            "name": "Updated Assessment",
            "type": AssessmentType.INITIAL,
            "module": self.module.id,
            "max_questions_at_once": 5,
            "max_retries": 1
        }
        response = self.send_auth_request("put", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)

    def test_update_module_assessment_without_module_error(self):
        url = f"{self.dashboard_url}/assessments/{self.module_assessment.id}/"
        data = {
            "name": "Updated Assessment",
            "type": AssessmentType.MODULE,
            "max_questions_at_once": 5,
            "max_retries": 3
        }
        response = self.send_auth_request("put", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)

    def test_update_assessment_empty_name(self):
        url = f"{self.dashboard_url}/assessments/{self.initial_assessment.id}/"
        data = {
            "name": "",
            "type": AssessmentType.INITIAL,
            "max_questions_at_once": 5,
            "max_retries": 1
        }
        response = self.send_auth_request("put", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.data)

    def test_update_assessment_not_found(self):
        url = f"{self.dashboard_url}/assessments/non-existent-id/"
        data = {
            "name": "Updated Assessment",
            "type": AssessmentType.INITIAL,
            "max_questions_at_once": 5,
            "max_retries": 1
        }
        response = self.send_auth_request("put", url, data=data)

        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.data.get("detail").lower())

    def test_delete_assessment_success(self):
        url = f"{self.dashboard_url}/assessments/{self.initial_assessment.id}/"
        response = self.send_auth_request("delete", url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data.get("detail"), "Assessment deleted successfully.")

    def test_delete_assessment_not_found(self):
        url = f"{self.dashboard_url}/assessments/non-existent-id/"
        response = self.send_auth_request("delete", url)

        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.data.get("detail").lower()) 