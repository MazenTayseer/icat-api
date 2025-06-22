from django.urls import path

from apps.simulator.views import UserPhishingScenarioUpdateView

urlpatterns = [
    path(
        '<str:scenario_id>/update/',
        UserPhishingScenarioUpdateView.as_view(),
        name='user-phishing-scenario-update'
    ),
]
