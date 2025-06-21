from django.urls import path

from apps.dashboard.rest.views.assessment import (
    AssessmentDashboardDetailView, AssessmentDashboardListView)
from apps.dashboard.rest.views.leaderboard import (LeaderboardDetailView,
                                                   LeaderboardView)
from apps.dashboard.rest.views.module import ModuleDashboardView
from apps.dashboard.rest.views.user_assessment import (
    AssessmentSubmissionView, UserAssessmentDetailView, UserAssessmentListView)
from apps.dashboard.rest.views.question import McqQuestionView, EssayQuestionView
from apps.dashboard.rest.views.answer import McqAnswerView, EssayAnswerRubricView

urlpatterns = [
    path('modules/', ModuleDashboardView.as_view(), name='get-all-modules'),
    path('modules/<str:id>/', ModuleDashboardView.as_view(), name='get-module'),

    path('assessments/', AssessmentDashboardListView.as_view(), name='get-all-assessments'),
    path('assessments/<str:id>/', AssessmentDashboardDetailView.as_view(), name='get-assessment'),

    path('questions/mcq/', McqQuestionView.as_view(), name='get-all-mcq-questions'),
    path('questions/mcq/<str:id>/', McqQuestionView.as_view(), name='get-mcq-question'),
    path('questions/essay/', EssayQuestionView.as_view(), name='get-all-essay-questions'),
    path('questions/essay/<str:id>/', EssayQuestionView.as_view(), name='get-essay-question'),

    path('answers/mcq/', McqAnswerView.as_view(), name='get-all-mcq-answers'),
    path('answers/mcq/<str:id>/', McqAnswerView.as_view(), name='get-mcq-answer'),
    path('answers/essay-rubric/', EssayAnswerRubricView.as_view(), name='get-all-essay-rubrics'),
    path('answers/essay-rubric/<str:id>/', EssayAnswerRubricView.as_view(), name='get-essay-rubric'),

    path('leaderboard/', LeaderboardView.as_view(), name='get-leaderboard'),
    path('leaderboard/<str:type>/', LeaderboardDetailView.as_view(), name='get-leaderboard-detail'),

    path('assessments/<str:assessment_id>/submit/', AssessmentSubmissionView.as_view(), name='submit-assessment'),

    path('assessments/<str:assessment_id>/submissions/', UserAssessmentListView.as_view(), name='list-user-submissions'),
    path('submissions/<str:submission_id>/', UserAssessmentDetailView.as_view(), name='get-user-submission'),
]
