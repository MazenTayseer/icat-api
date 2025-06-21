from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dal.models.enums.initial_assessment_domain import InitialAssessmentDomain
from apps.dashboard.tests.base import DashboardBaseTestCase
from common.tests.factory import AssessmentFactory, ModuleFactory


class QuestionCreationTestCase(DashboardBaseTestCase):
    def setUp(self):
        super().setUp()
        self.module = ModuleFactory()
        self.initial_assessment = AssessmentFactory(
            name='Initial Assessment',
            type=AssessmentType.INITIAL,
            module=None
        )
        self.module_assessment = AssessmentFactory(
            name='Module Assessment',
            type=AssessmentType.MODULE,
            module=self.module
        )

    def test_create_mcq_question_initial_assessment_success(self):
        url = f"{self.dashboard_url}/questions/mcq/"
        data = {
            "assessment": self.initial_assessment.id,
            "domain": InitialAssessmentDomain.PHISHING,
            "difficulty": 3,
            "text": "What should you do if you receive a suspicious email?"
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("text"), "What should you do if you receive a suspicious email?")
        self.assertEqual(response.data.get("domain"), InitialAssessmentDomain.PHISHING)
        self.assertEqual(response.data.get("difficulty"), 3)
        self.assertEqual(response.data.get("assessment"), self.initial_assessment.id)

    def test_create_mcq_question_module_assessment_success(self):
        url = f"{self.dashboard_url}/questions/mcq/"
        data = {
            "assessment": self.module_assessment.id,
            "difficulty": 2,
            "text": "What is the best practice for password creation?"
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("text"), "What is the best practice for password creation?")
        self.assertIsNone(response.data.get("domain"))
        self.assertEqual(response.data.get("difficulty"), 2)
        self.assertEqual(response.data.get("assessment"), self.module_assessment.id)

    def test_create_essay_question_initial_assessment_success(self):
        url = f"{self.dashboard_url}/questions/essay/"
        data = {
            "assessment": self.initial_assessment.id,
            "domain": InitialAssessmentDomain.PASSWORD,
            "difficulty": 4,
            "text": "Explain why strong passwords are important for cybersecurity."
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("text"), "Explain why strong passwords are important for cybersecurity.")
        self.assertEqual(response.data.get("domain"), InitialAssessmentDomain.PASSWORD)
        self.assertEqual(response.data.get("difficulty"), 4)
        self.assertEqual(response.data.get("assessment"), self.initial_assessment.id)

    def test_create_essay_question_module_assessment_success(self):
        url = f"{self.dashboard_url}/questions/essay/"
        data = {
            "assessment": self.module_assessment.id,
            "difficulty": 3,
            "text": "Describe the steps to identify a phishing attempt."
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("text"), "Describe the steps to identify a phishing attempt.")
        self.assertIsNone(response.data.get("domain"))
        self.assertEqual(response.data.get("difficulty"), 3)
        self.assertEqual(response.data.get("assessment"), self.module_assessment.id)

    def test_create_question_empty_text(self):
        url = f"{self.dashboard_url}/questions/mcq/"
        data = {
            "assessment": self.initial_assessment.id,
            "domain": InitialAssessmentDomain.PHISHING,
            "difficulty": 3,
            "text": ""
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("text", response.data)

    def test_create_question_invalid_difficulty(self):
        url = f"{self.dashboard_url}/questions/mcq/"
        data = {
            "assessment": self.initial_assessment.id,
            "domain": InitialAssessmentDomain.PHISHING,
            "difficulty": 6,
            "text": "What should you do if you receive a suspicious email?"
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("difficulty", response.data) 