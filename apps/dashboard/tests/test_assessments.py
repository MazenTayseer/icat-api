from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dashboard.tests.base import DashboardBaseTestCase
from common.tests.factory import (AssessmentFactory, McqAnswerFactory,
                                  McqQuestionFactory, ModuleFactory)


class AssessmentsTestCases(DashboardBaseTestCase):
    def setUp(self):
        self.module = ModuleFactory()
        self.assessment_1 = AssessmentFactory(
            name='Assessment 1',
            module=self.module,
            type=AssessmentType.MODULE
        )
        self.assessment_2 = AssessmentFactory(
            name='Assessment 2',
            module=self.module,
            type=AssessmentType.MODULE
        )

        self.question_1_1 = McqQuestionFactory(assessment=self.assessment_1)
        self.question_1_2 = McqQuestionFactory(assessment=self.assessment_1)

        McqAnswerFactory(question=self.question_1_1, is_correct=True)
        McqAnswerFactory(question=self.question_1_1, is_correct=False)

        McqAnswerFactory(question=self.question_1_2, is_correct=True)
        McqAnswerFactory(question=self.question_1_2, is_correct=False)
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
        self.assertEqual(response.data.get("questions")[0].get("type"), "mcq")
