

from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dashboard.tests.base import DashboardBaseTestCase
from common.tests.factory import (AssessmentFactory,
                                  EssayAnswerSubmissionFactory,
                                  EssayQuestionFactory, McqAnswerFactory,
                                  McqAnswerSubmissionFactory,
                                  McqQuestionFactory, UserAssessmentFactory)


class UserAssessmentEndpointsTestCase(DashboardBaseTestCase):
    def setUp(self):
        super().setUp()

        self.assessment = AssessmentFactory(type=AssessmentType.INITIAL, module=None)

        self.mcq_question = McqQuestionFactory(assessment=self.assessment)
        self.mcq_answer = McqAnswerFactory(question=self.mcq_question, is_correct=True)
        self.essay_question = EssayQuestionFactory(assessment=self.assessment)

        self.user_assessment = UserAssessmentFactory(
            user=self.user,
            assessment=self.assessment,
        )

        McqAnswerSubmissionFactory(
            user_assessment=self.user_assessment,
            question=self.mcq_question,
            answer=self.mcq_answer,
        )

        EssayAnswerSubmissionFactory(
            user_assessment=self.user_assessment,
            question=self.essay_question,
        )

    def test_list_user_submissions_for_assessment(self):
        url = f"{self.dashboard_url}/assessments/{self.assessment.id}/submissions/"
        response = self.send_auth_request("get", url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_single_user_submission(self):
        url = f"{self.dashboard_url}/submissions/{self.user_assessment.id}/"
        response = self.send_auth_request("get", url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.user_assessment.id)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["assessment"], self.assessment.id)
