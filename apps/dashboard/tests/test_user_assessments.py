
from apps.dashboard.tests.base import DashboardBaseTestCase
from apps.dashboard.tests.factory import (AnswerFactory, AssessmentFactory,
                                          ModuleFactory, QuestionFactory)


class AssessmentsTestCases(DashboardBaseTestCase):
    def setUp(self):
        self.module = ModuleFactory()
        self.assessment = AssessmentFactory(name='Assessment 1', module=self.module)
        self.question = QuestionFactory(assessment=self.assessment)
        self.answer_1 = AnswerFactory(question=self.question, is_correct=True)
        self.answer_2 = AnswerFactory(question=self.question, is_correct=False)

        self.question_2 = QuestionFactory(assessment=self.assessment)
        self.answer_3 = AnswerFactory(question=self.question_2, is_correct=True)
        self.answer_4 = AnswerFactory(question=self.question_2, is_correct=False)
        super().setUp()

    def test_submit_assessment_all_true(self):
        url = f"{self.dashboard_url}/assessments/{self.assessment.id}/submit/"
        data = {
            "answers": [
                {"question_id": self.question.id, "answer_id": self.answer_1.id},
                {"question_id": self.question_2.id, "answer_id": self.answer_3.id}
            ]
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data.get("is_passed"))
        self.assertEqual(response.data.get("score"), 2)
        self.assertEqual(response.data.get("score_percentage"), 100)

    def test_submit_assessment_all_false(self):
        url = f"{self.dashboard_url}/assessments/{self.assessment.id}/submit/"
        data = {
            "answers": [
                {"question_id": self.question.id, "answer_id": self.answer_2.id},
                {"question_id": self.question_2.id, "answer_id": self.answer_4.id}
            ]
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.data.get("is_passed"))
        self.assertEqual(response.data.get("score"), 0)
        self.assertEqual(response.data.get("score_percentage"), 0)

    def test_submit_assessment_mixed(self):
        url = f"{self.dashboard_url}/assessments/{self.assessment.id}/submit/"
        data = {
            "answers": [
                {"question_id": self.question.id, "answer_id": self.answer_1.id},
                {"question_id": self.question_2.id, "answer_id": self.answer_4.id}
            ]
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data.get("is_passed"))
        self.assertEqual(response.data.get("score"), 1)
        self.assertEqual(response.data.get("score_percentage"), 50)
