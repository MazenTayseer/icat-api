
from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dashboard.tests.base import DashboardBaseTestCase
from common.tests.decorators import mock_user_asessments_clients
from common.tests.factory import (AssessmentFactory, EssayAnswerRubricFactory,
                                  EssayQuestionFactory, McqAnswerFactory,
                                  McqQuestionFactory, ModuleFactory)


class AssessmentsTestCases(DashboardBaseTestCase):
    def setUp(self):
        self.module = ModuleFactory()
        self.assessment = AssessmentFactory(name='Assessment 1', module=self.module, type=AssessmentType.MODULE)
        self.question_mcq = McqQuestionFactory(
            assessment=self.assessment,
            text="Which of the following is a strong password?"
        )
        self.answer_mcq_1 = McqAnswerFactory(
            question=self.question_mcq,
            text="P@ssw0rd123!",
            is_correct=True
        )
        self.answer_mcq_2 = McqAnswerFactory(
            question=self.question_mcq,
            text="123456",
            is_correct=False
        )

        self.question_essay = EssayQuestionFactory(
            assessment=self.assessment,
            text="Explain why it’s important to avoid clicking on suspicious email links."
        )
        self.answer_essay_1a = EssayAnswerRubricFactory(
            question=self.question_essay,
            text="Mentions risk of phishing or malware",
            weight=1.0
        )
        self.answer_essay_1b = EssayAnswerRubricFactory(
            question=self.question_essay,
            text="Explains how attackers trick users into revealing information",
            weight=0.5
        )
        self.answer_essay_1c = EssayAnswerRubricFactory(
            question=self.question_essay,
            text="Suggests verifying links before clicking",
            weight=0.5
        )

        self.question_essay_2 = EssayQuestionFactory(
            assessment=self.assessment,
            text="Describe two ways to protect your online accounts."
        )
        self.answer_essay_2a = EssayAnswerRubricFactory(
            question=self.question_essay_2,
            text="Mentions using strong and unique passwords",
            weight=1.0
        )
        self.answer_essay_2b = EssayAnswerRubricFactory(
            question=self.question_essay_2,
            text="Mentions enabling two-factor authentication",
            weight=1.0
        )

        super().setUp()

    @mock_user_asessments_clients
    def test_submit_assessment_all_true(self, mock_gemini_instance, _):
        url = f"{self.dashboard_url}/assessments/{self.assessment.id}/submit/"
        data = {
            "answers": {
                "mcq": [
                    {"question": self.question_mcq.id, "answer": self.answer_mcq_1.id},
                ],
                "essay": [
                    {
                        "question": self.question_essay.id,
                        "answer": "Clicking on suspicious links can lead to phishing attacks or malware infections."
                    },
                    {
                        "question": self.question_essay_2.id,
                        "answer": "I use strong passwords and enable two-factor authentication to secure my accounts."
                    },
                ]
            }
        }
        response = self.send_auth_request("post", url, data=data)

        self.assertEqual(mock_gemini_instance.chat.call_count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("score"))
        self.assertIsNotNone(response.data.get("percentage"))
        self.assertEqual(len(response.data.get("answers").get("mcq")), 1)
        self.assertEqual(len(response.data.get("answers").get("essay")), 2)
