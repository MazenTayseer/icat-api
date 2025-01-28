
from apps.dashboard.tests.base import DashboardBaseTestCase
from apps.dashboard.tests.factory import (AnswerFactory, AssessmentFactory,
                                          ModuleFactory, QuestionFactory)


class AssessmentsTestCases(DashboardBaseTestCase):
    def setUp(self):
        self.module = ModuleFactory()
        self.assessment_1 = AssessmentFactory(name='Assessment 1', module=self.module)
        self.assessment_2 = AssessmentFactory(name='Assessment 2', module=self.module)

        self.question_1_1 = QuestionFactory(assessment=self.assessment_1)
        self.question_1_2 = QuestionFactory(assessment=self.assessment_1)

        AnswerFactory(question=self.question_1_1)
        AnswerFactory(question=self.question_1_1)

        AnswerFactory(question=self.question_1_2)
        AnswerFactory(question=self.question_1_2)
        super().setUp()

    def test_get_all_assessment(self):
        url = f"{self.dashboard_url}/assessments/"
        response = self.send_auth_request("get", url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_one_assessment(self):
        url = f"{self.dashboard_url}/assessments/{self.assessment_1.id}/"
        response = self.send_auth_request("get", url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("id"), self.assessment_1.id)
        self.assertEqual(response.data.get("name"), 'Assessment 1')
        self.assertEqual(response.data.get("module"), self.module.id)
        self.assertEqual(len(response.data.get("questions")), 2)
        self.assertEqual(len(response.data.get("questions")[0].get("answers")), 2)
