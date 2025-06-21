from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dashboard.tests.base import DashboardBaseTestCase
from common.tests.factory import AssessmentFactory, ModuleFactory, McqQuestionFactory, EssayQuestionFactory


class AnswerCreationTestCase(DashboardBaseTestCase):
    def setUp(self):
        super().setUp()
        self.module = ModuleFactory()
        self.assessment = AssessmentFactory(
            name='Test Assessment',
            type=AssessmentType.MODULE,
            module=self.module
        )
        self.mcq_question = McqQuestionFactory(assessment=self.assessment)
        self.essay_question = EssayQuestionFactory(assessment=self.assessment)

    def test_create_mcq_answer_success(self):
        url = f"{self.dashboard_url}/answers/mcq/"
        data = {
            "question": self.mcq_question.id,
            "text": "This is the correct answer",
            "is_correct": True
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("text"), "This is the correct answer")
        self.assertTrue(response.data.get("is_correct"))
        self.assertEqual(response.data.get("question"), self.mcq_question.id)

    def test_create_mcq_answer_incorrect(self):
        url = f"{self.dashboard_url}/answers/mcq/"
        data = {
            "question": self.mcq_question.id,
            "text": "This is an incorrect answer",
            "is_correct": False
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("text"), "This is an incorrect answer")
        self.assertFalse(response.data.get("is_correct"))
        self.assertEqual(response.data.get("question"), self.mcq_question.id)

    def test_create_essay_rubric_success(self):
        url = f"{self.dashboard_url}/answers/essay-rubric/"
        data = {
            "question": self.essay_question.id,
            "text": "Mentions cybersecurity best practices",
            "weight": 1.0
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("text"), "Mentions cybersecurity best practices")
        self.assertEqual(response.data.get("weight"), 1.0)
        self.assertEqual(response.data.get("question"), self.essay_question.id)

    def test_create_essay_rubric_with_fractional_weight(self):
        url = f"{self.dashboard_url}/answers/essay-rubric/"
        data = {
            "question": self.essay_question.id,
            "text": "Provides specific examples",
            "weight": 0.5
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("text"), "Provides specific examples")
        self.assertEqual(response.data.get("weight"), 0.5)
        self.assertEqual(response.data.get("question"), self.essay_question.id)

    def test_create_mcq_answer_empty_text(self):
        url = f"{self.dashboard_url}/answers/mcq/"
        data = {
            "question": self.mcq_question.id,
            "text": "",
            "is_correct": True
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("text", response.data)

    def test_create_essay_rubric_empty_text(self):
        url = f"{self.dashboard_url}/answers/essay-rubric/"
        data = {
            "question": self.essay_question.id,
            "text": "",
            "weight": 1.0
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("text", response.data)

    def test_create_essay_rubric_invalid_weight(self):
        url = f"{self.dashboard_url}/answers/essay-rubric/"
        data = {
            "question": self.essay_question.id,
            "text": "Valid rubric text",
            "weight": 0
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("weight", response.data)

    def test_create_essay_rubric_negative_weight(self):
        url = f"{self.dashboard_url}/answers/essay-rubric/"
        data = {
            "question": self.essay_question.id,
            "text": "Valid rubric text",
            "weight": -1.0
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("weight", response.data) 