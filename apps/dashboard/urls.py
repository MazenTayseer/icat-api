from django.urls import path

from apps.dashboard.rest.assessments.views import (
    AssessmentDashboardDetailView, AssessmentDashboardListView)
from apps.dashboard.rest.modules.views import ModuleDashboardView
from apps.dashboard.rest.user_assessment.views import AssessmentSubmissionView

urlpatterns = [
    path('modules/', ModuleDashboardView.as_view(), name='get-all-modules'),
    path('modules/<str:id>/', ModuleDashboardView.as_view(), name='get-module'),

    path('assessments/', AssessmentDashboardListView.as_view(), name='get-all-assessments'),
    path('assessments/<str:id>/', AssessmentDashboardDetailView.as_view(), name='get-assessment'),

    path('assessments/<str:assessment_id>/submit/', AssessmentSubmissionView.as_view(), name='submit-assessment'),
]
