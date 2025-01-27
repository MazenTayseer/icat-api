from django.urls import path

from apps.dashboard.rest.modules.views import ModuleDashboardView

urlpatterns = [
    path('modules/', ModuleDashboardView.as_view(), name='get-all-modules'),
    path('modules/<str:id>/', ModuleDashboardView.as_view(), name='get-module'),
]
