# from django.utils import timezone
# from datetime import timedelta

# from apps.dal.models.enums.assessment_type import AssessmentType
# from apps.dashboard.tests.base import DashboardBaseTestCase
# from common.tests.factory import (
#     AssessmentFactory, UserAssessmentFactory,
#     McqAnswerSubmissionFactory, EssayAnswerSubmissionFactory,
#     McqQuestionFactory, EssayQuestionFactory, McqAnswerFactory
# )


# class UserAssessmentEndpointsTestCase(DashboardBaseTestCase):
#     def setUp(self):
#         super().setUp()

#         self.assessment = AssessmentFactory(
#             name="Initial Security Assessment",
#             type=AssessmentType.INITIAL
#         )

#         self.mcq_question = McqQuestionFactory(assessment=self.assessment)
#         self.mcq_answer = McqAnswerFactory(question=self.mcq_question, is_correct=True)
#         self.essay_question = EssayQuestionFactory(assessment=self.assessment)

#         self.user_assessment = UserAssessmentFactory(
#             user=self.user,
#             assessment=self.assessment,
#             score=8.5,
#             max_score=10.0,
#             trial=1,
#             feedback="Good performance",
#             created_at=timezone.now() - timedelta(days=1)
#         )

#         McqAnswerSubmissionFactory(
#             user_assessment=self.user_assessment,
#             question=self.mcq_question,
#             answer=self.mcq_answer,
#             score=1.0,
#             max_score=1.0
#         )

#         EssayAnswerSubmissionFactory(
#             user_assessment=self.user_assessment,
#             question=self.essay_question,
#             answer="My essay answer about cybersecurity.",
#             score=7.5,
#             max_score=9.0
#         )

#     def test_list_user_submissions_for_assessment(self):
#         url = f"{self.dashboard_url}/submissions/{self.assessment.id}/"
#         response = self.send_auth_request("get", url)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), 1)

#         submission = response.data[0]
#         self.assertEqual(submission["id"], self.user_assessment.id)
#         self.assertEqual(submission["user"], self.user.id)
#         self.assertEqual(submission["assessment"], self.assessment.id)
#         self.assertEqual(submission["score"], 8.5)
#         self.assertEqual(submission["max_score"], 10.0)
#         self.assertEqual(submission["trial"], 1)
#         self.assertEqual(submission["feedback"], "Good performance")

#         # Check calculated fields
#         self.assertEqual(submission["percentage"], 85.0)
#         self.assertTrue(submission["is_passed"])

#         # Check answers structure
#         self.assertIn("answers", submission)
#         self.assertIn("mcq", submission["answers"])
#         self.assertIn("essay", submission["answers"])
#         self.assertEqual(len(submission["answers"]["mcq"]), 1)
#         self.assertEqual(len(submission["answers"]["essay"]), 1)

#     def test_get_single_user_submission(self):
#         """Test GET /submissions/{submission_id}/ - Get specific user submission detail"""
#         url = f"{self.dashboard_url}/submissions/{self.user_assessment.id}/"
#         response = self.send_auth_request("get", url)

#         self.assertEqual(response.status_code, 200)

#         # Verify response data
#         self.assertEqual(response.data["id"], self.user_assessment.id)
#         self.assertEqual(response.data["user"], self.user.id)
#         self.assertEqual(response.data["assessment"], self.assessment.id)
#         self.assertEqual(response.data["score"], 8.5)
#         self.assertEqual(response.data["max_score"], 10.0)
#         self.assertEqual(response.data["trial"], 1)
#         self.assertEqual(response.data["feedback"], "Good performance")
#         self.assertEqual(response.data["percentage"], 85.0)
#         self.assertTrue(response.data["is_passed"])

#         # Verify answers are included
#         answers = response.data["answers"]
#         self.assertEqual(len(answers["mcq"]), 1)
#         self.assertEqual(len(answers["essay"]), 1)

#         # Check MCQ answer details
#         mcq_answer = answers["mcq"][0]
#         self.assertEqual(mcq_answer["score"], 1.0)
#         self.assertEqual(mcq_answer["max_score"], 1.0)

#         # Check Essay answer details
#         essay_answer = answers["essay"][0]
#         self.assertEqual(essay_answer["score"], 7.5)
#         self.assertEqual(essay_answer["max_score"], 9.0)
#         self.assertEqual(essay_answer["answer"], "My essay answer about cybersecurity.")
