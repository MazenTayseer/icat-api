from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dashboard.tests.base import DashboardBaseTestCase
from common.tests.factory import AssessmentFactory, ModuleFactory, McqQuestionFactory, McqAnswerFactory


class AssessmentDetailFixTestCase(DashboardBaseTestCase):
    def setUp(self):
        super().setUp()
        self.module = ModuleFactory()
        self.assessment = AssessmentFactory(
            name='Test Assessment',
            type=AssessmentType.MODULE,
            module=self.module,
            max_questions_at_once=5
        )
        self.question = McqQuestionFactory(assessment=self.assessment)
        self.answer = McqAnswerFactory(question=self.question, is_correct=True)

    def test_get_assessment_detail_with_questions(self):
        """Test that assessment detail endpoint works with questions"""
        url = f"{self.dashboard_url}/assessments/{self.assessment.id}/"
        response = self.send_auth_request("get", url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("id"), self.assessment.id)
        self.assertEqual(response.data.get("name"), 'Test Assessment')
        self.assertIn("questions", response.data)
        self.assertIsInstance(response.data.get("questions"), list)

    def test_get_assessment_detail_without_questions(self):
        """Test that assessment detail endpoint works without questions"""
        assessment_without_questions = AssessmentFactory(
            name='Assessment Without Questions',
            type=AssessmentType.INITIAL,
            module=None,
            max_questions_at_once=5
        )
        
        url = f"{self.dashboard_url}/assessments/{assessment_without_questions.id}/"
        response = self.send_auth_request("get", url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("id"), assessment_without_questions.id)
        self.assertEqual(response.data.get("name"), 'Assessment Without Questions')
        self.assertIn("questions", response.data)
        self.assertIsInstance(response.data.get("questions"), list)
        self.assertEqual(len(response.data.get("questions")), 0) 