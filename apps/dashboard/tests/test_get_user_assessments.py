# from django.utils import timezone
# from datetime import timedelta

# from apps.dal.models.enums.assessment_type import AssessmentType
# from apps.dal.models.user_assessment import UserAssessments
# from apps.dashboard.tests.base import DashboardBaseTestCase
# from common.tests.factory import (
#     AssessmentFactory, ModuleFactory, UserFactory, UserAssessmentFactory,
#     McqAnswerSubmissionFactory, EssayAnswerSubmissionFactory,
#     McqQuestionFactory, EssayQuestionFactory, McqAnswerFactory, EssayAnswerRubricFactory
# )


# class UserAssessmentEndpointsTestCase(DashboardBaseTestCase):
#     def setUp(self):
#         super().setUp()

#         self.module1 = ModuleFactory(name="Cybersecurity Basics")
#         self.module2 = ModuleFactory(name="Advanced Security")

#         self.assessment1 = AssessmentFactory(
#             name="Initial Security Assessment",
#             module=None,
#             type=AssessmentType.INITIAL
#         )
#         self.assessment2 = AssessmentFactory(
#             name="Module 1 Assessment",
#             module=self.module1,
#             type=AssessmentType.MODULE
#         )
#         self.assessment3 = AssessmentFactory(
#             name="Module 2 Assessment",
#             module=self.module2,
#             type=AssessmentType.MODULE
#         )

#         self.mcq_question = McqQuestionFactory(assessment=self.assessment1)
#         self.mcq_answer = McqAnswerFactory(question=self.mcq_question, is_correct=True)

#         self.essay_question = EssayQuestionFactory(assessment=self.assessment1)
#         self.essay_rubric = EssayAnswerRubricFactory(question=self.essay_question, weight=2.0)

#         self.other_user = UserFactory(email="other@test.com", password="Test1234")

#         self.user_assessment1 = UserAssessmentFactory(
#             user=self.user,
#             assessment=self.assessment1,
#             score=8.5,
#             max_score=10.0,
#             trial=1,
#             feedback="Good overall performance",
#             created_at=timezone.now() - timedelta(days=2)
#         )

#         self.user_assessment2 = UserAssessmentFactory(
#             user=self.user,
#             assessment=self.assessment1,
#             score=9.0,
#             max_score=10.0,
#             trial=2,
#             feedback="Excellent improvement",
#             created_at=timezone.now() - timedelta(days=1)
#         )

#         self.user_assessment3 = UserAssessmentFactory(
#             user=self.user,
#             assessment=self.assessment2,
#             score=7.0,
#             max_score=10.0,
#             trial=1,
#             feedback="Needs more practice",
#             created_at=timezone.now()
#         )

#         # Create assessment for other user (should not be accessible)
#         self.other_user_assessment = UserAssessmentFactory(
#             user=self.other_user,
#             assessment=self.assessment1,
#             score=6.0,
#             max_score=10.0,
#             trial=1
#         )

#         # Create answer submissions for testing
#         self.mcq_submission = McqAnswerSubmissionFactory(
#             user_assessment=self.user_assessment1,
#             question=self.mcq_question,
#             answer=self.mcq_answer,
#             score=1.0,
#             max_score=1.0,
#             feedback="Correct answer"
#         )

#         self.essay_submission = EssayAnswerSubmissionFactory(
#             user_assessment=self.user_assessment1,
#             question=self.essay_question,
#             answer="This is my essay answer about cybersecurity best practices.",
#             score=7.5,
#             max_score=9.0,
#             feedback="Good analysis but could be more detailed"
#         )

#     def test_list_user_submissions_for_assessment_success(self):
#         """Test listing user submissions for a specific assessment"""
#         url = f"{self.dashboard_url}/submissions/{self.assessment1.id}/"
#         response = self.send_auth_request("get", url)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), 2)  # Two trials for assessment1

#         # Check data is ordered by created_at (most recent first)
#         self.assertEqual(response.data[0]["trial"], 2)
#         self.assertEqual(response.data[1]["trial"], 1)

#         # Verify response structure
#         first_submission = response.data[0]
#         self.assertIn("id", first_submission)
#         self.assertIn("score", first_submission)
#         self.assertIn("max_score", first_submission)
#         self.assertIn("trial", first_submission)
#         self.assertIn("feedback", first_submission)
#         self.assertIn("percentage", first_submission)
#         self.assertIn("is_passed", first_submission)
#         self.assertIn("answers", first_submission)
#         self.assertEqual(first_submission["user"], self.user.id)
#         self.assertEqual(first_submission["assessment"], self.assessment1.id)

#     def test_list_user_submissions_for_assessment_no_submissions(self):
#         """Test listing submissions for assessment with no user submissions"""
#         url = f"{self.dashboard_url}/submissions/{self.assessment3.id}/"
#         response = self.send_auth_request("get", url)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), 0)

#     def test_list_user_submissions_for_nonexistent_assessment(self):
#         """Test listing submissions for non-existent assessment"""
#         url = f"{self.dashboard_url}/submissions/nonexistent-id/"
#         response = self.send_auth_request("get", url)

#         self.assertEqual(response.status_code, 404)
#         self.assertIn("Assessment not found", response.data["detail"])

#     def test_list_user_submissions_unauthorized(self):
#         """Test listing submissions without authentication"""
#         url = f"{self.dashboard_url}/submissions/{self.assessment1.id}/"
#         response = self.send_unauth_request("get", url)

#         self.assertEqual(response.status_code, 401)

#     def test_list_user_submissions_only_returns_current_user_data(self):
#         """Test that endpoint only returns current user's submissions"""
#         url = f"{self.dashboard_url}/submissions/{self.assessment1.id}/"
#         response = self.send_auth_request("get", url)

#         self.assertEqual(response.status_code, 200)

#         # Should only return current user's submissions, not other_user's
#         user_ids = [submission["user"] for submission in response.data]
#         self.assertTrue(all(user_id == self.user.id for user_id in user_ids))
#         self.assertNotIn(self.other_user.id, user_ids)

#     def test_get_user_submission_detail_success(self):
#         """Test getting a specific user submission by ID"""
#         url = f"{self.dashboard_url}/submissions/{self.user_assessment1.id}/"
#         response = self.send_auth_request("get", url)

#         self.assertEqual(response.status_code, 200)

#         # Verify response structure
#         self.assertEqual(response.data["id"], self.user_assessment1.id)
#         self.assertEqual(response.data["user"], self.user.id)
#         self.assertEqual(response.data["assessment"], self.assessment1.id)
#         self.assertEqual(response.data["score"], 8.5)
#         self.assertEqual(response.data["max_score"], 10.0)
#         self.assertEqual(response.data["trial"], 1)
#         self.assertEqual(response.data["feedback"], "Good overall performance")
#         self.assertIn("percentage", response.data)
#         self.assertIn("is_passed", response.data)

#         # Verify answers structure
#         self.assertIn("answers", response.data)
#         answers = response.data["answers"]
#         self.assertIn("mcq", answers)
#         self.assertIn("essay", answers)

#         # Check MCQ answers
#         self.assertEqual(len(answers["mcq"]), 1)
#         mcq_answer = answers["mcq"][0]
#         self.assertEqual(mcq_answer["score"], 1.0)
#         self.assertEqual(mcq_answer["feedback"], "Correct answer")

#         # Check Essay answers
#         self.assertEqual(len(answers["essay"]), 1)
#         essay_answer = answers["essay"][0]
#         self.assertEqual(essay_answer["score"], 7.5)
#         self.assertEqual(essay_answer["answer"], "This is my essay answer about cybersecurity best practices.")
#         self.assertEqual(essay_answer["feedback"], "Good analysis but could be more detailed")

#     def test_get_user_submission_detail_nonexistent(self):
#         """Test getting a non-existent submission"""
#         url = f"{self.dashboard_url}/submissions/nonexistent-id/"
#         response = self.send_auth_request("get", url)

#         self.assertEqual(response.status_code, 404)
#         self.assertIn("Submission not found", response.data["detail"])

#     def test_get_user_submission_detail_other_user(self):
#         """Test accessing another user's submission (should fail)"""
#         url = f"{self.dashboard_url}/submissions/{self.other_user_assessment.id}/"
#         response = self.send_auth_request("get", url)

#         # This should return 404 since the current implementation doesn't check ownership
#         # But ideally should check ownership and return 403 or 404
#         self.assertEqual(response.status_code, 404)

#     def test_get_user_submission_detail_unauthorized(self):
#         """Test getting submission detail without authentication"""
#         url = f"{self.dashboard_url}/submissions/{self.user_assessment1.id}/"
#         response = self.send_unauth_request("get", url)

#         self.assertEqual(response.status_code, 401)

#     def test_user_assessment_properties(self):
#         """Test UserAssessment model properties"""
#         # Test percentage calculation
#         assessment = UserAssessments.objects.get(id=self.user_assessment1.id)
#         expected_percentage = (8.5 / 10.0) * 100
#         self.assertEqual(assessment.percentage, expected_percentage)

#         # Test is_passed property (should pass with 85%)
#         self.assertTrue(assessment.is_passed)

#         # Test failed assessment
#         failed_assessment = UserAssessmentFactory(
#             user=self.user,
#             assessment=self.assessment2,
#             score=3.0,
#             max_score=10.0,
#             trial=2
#         )
#         failed_assessment.save()
#         self.assertFalse(failed_assessment.is_passed)  # 30% < 50%

#     def test_assessment_with_no_answers(self):
#         """Test assessment submission with no answer submissions"""
#         assessment_no_answers = UserAssessmentFactory(
#             user=self.user,
#             assessment=self.assessment3,
#             score=0.0,
#             max_score=5.0,
#             trial=1
#         )

#         url = f"{self.dashboard_url}/submissions/{assessment_no_answers.id}/"
#         response = self.send_auth_request("get", url)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data["answers"]["mcq"]), 0)
#         self.assertEqual(len(response.data["answers"]["essay"]), 0)

#     def test_multiple_trials_ordering(self):
#         """Test that multiple trials are properly ordered by creation date"""
#         # Create additional trials with specific timestamps
#         trial3 = UserAssessmentFactory(
#             user=self.user,
#             assessment=self.assessment2,
#             score=8.0,
#             max_score=10.0,
#             trial=3,
#             created_at=timezone.now() - timedelta(hours=1)
#         )

#         trial4 = UserAssessmentFactory(
#             user=self.user,
#             assessment=self.assessment2,
#             score=9.5,
#             max_score=10.0,
#             trial=4,
#             created_at=timezone.now()
#         )

#         url = f"{self.dashboard_url}/submissions/{self.assessment2.id}/"
#         response = self.send_auth_request("get", url)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), 3)  # Original + 2 new trials

#         # Check ordering (most recent first)
#         trials = [submission["trial"] for submission in response.data]
#         self.assertEqual(trials, [4, 3, 1])  # Most recent to oldest

#         # Check scores are correct
#         scores = [submission["score"] for submission in response.data]
#         self.assertEqual(scores, [9.5, 8.0, 7.0])

#     def test_response_includes_calculated_fields(self):
#         """Test that response includes calculated fields like percentage and is_passed"""
#         url = f"{self.dashboard_url}/submissions/{self.user_assessment1.id}/"
#         response = self.send_auth_request("get", url)

#         self.assertEqual(response.status_code, 200)

#         # Test percentage calculation
#         expected_percentage = (8.5 / 10.0) * 100
#         self.assertEqual(response.data["percentage"], expected_percentage)

#         # Test is_passed calculation
#         self.assertTrue(response.data["is_passed"])  # 85% > 50%

#         # Test with failed assessment
#         url = f"{self.dashboard_url}/submissions/{self.user_assessment3.id}/"
#         response = self.send_auth_request("get", url)

#         self.assertEqual(response.status_code, 200)
#         expected_percentage = (7.0 / 10.0) * 100
#         self.assertEqual(response.data["percentage"], expected_percentage)
#         self.assertTrue(response.data["is_passed"])  # 70% > 50%
