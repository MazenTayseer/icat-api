from django.urls import path

from apps.dashboard.rest.views.assessment import (
    AssessmentDashboardDetailView, AssessmentDashboardListView)
from apps.dashboard.rest.views.leaderboard import (LeaderboardDetailView,
                                                   LeaderboardView)
from apps.dashboard.rest.views.module import ModuleDashboardView
from apps.dashboard.rest.views.user_assessment import (
    AssessmentSubmissionView, UserAssessmentDetailView, UserAssessmentListView)

urlpatterns = [
    path('modules/', ModuleDashboardView.as_view(), name='get-all-modules'),
    path('modules/<str:id>/', ModuleDashboardView.as_view(), name='get-module'),

    path('assessments/', AssessmentDashboardListView.as_view(), name='get-all-assessments'),
    path('assessments/<str:id>/', AssessmentDashboardDetailView.as_view(), name='get-assessment'),

    path('leaderboard/', LeaderboardView.as_view(), name='get-leaderboard'),
    path('leaderboard/<str:id>/', LeaderboardDetailView.as_view(), name='get-leaderboard-detail'),

    path('assessments/<str:assessment_id>/submit/', AssessmentSubmissionView.as_view(), name='submit-assessment'),

    path('submissions/<str:submission_id>/', UserAssessmentDetailView.as_view(), name='get-user-submission'),
    path('submissions/<str:assessment_id>/', UserAssessmentListView.as_view(), name='list-user-submissions'),
]
