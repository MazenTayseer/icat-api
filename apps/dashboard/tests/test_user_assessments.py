
from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dashboard.tests.base import DashboardBaseTestCase
from common.tests.decorators import mock_ollama_for_assessment
from common.tests.factory import (AssessmentFactory, EssayAnswerRubricFactory,
                                  EssayQuestionFactory, McqAnswerFactory,
                                  McqQuestionFactory, ModuleFactory)


class AssessmentsTestCases(DashboardBaseTestCase):
    def setUp(self):
        self.module = ModuleFactory()
        self.assessment = AssessmentFactory(name='Assessment 1', module=self.module, type=AssessmentType.MODULE)
        self.question = McqQuestionFactory(assessment=self.assessment, text="MCQ Question")
        self.answer_1 = McqAnswerFactory(question=self.question, is_correct=True, text="MCQ Correct Answer 1")
        self.answer_2 = McqAnswerFactory(question=self.question, is_correct=False, text="MCQ Incorrect Answer 1")

        self.question_2 = EssayQuestionFactory(assessment=self.assessment, text="Essay Question")
        self.answer_3 = EssayAnswerRubricFactory(question=self.question_2, value=3, weight=1.0, text="Essay Answer 1")
        super().setUp()

    @mock_ollama_for_assessment
    def test_submit_assessment_all_true(self, mock_ollama_instance):
        url = f"{self.dashboard_url}/assessments/{self.assessment.id}/submit/"
        data = {
            "answers": {
                "mcq": [
                    {"question": self.question.id, "answer": self.answer_1.id},
                ],
                "essay": [
                    {"question": self.question_2.id, "answer": "Essay Answer 1"},
                ]
            },
            "assessment": self.assessment.id,
            "user": self.user.id
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(mock_ollama_instance.chat.call_count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("score"))
        self.assertIsNotNone(response.data.get("score_percentage"))
