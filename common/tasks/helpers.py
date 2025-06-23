from datetime import timedelta

from django.utils import timezone

from apps.dal.models import UserPhishingScenario
from apps.dal.models.enums.user_simulation_status import UserSimulationStatus


class TasksHelpers:
    @staticmethod
    def update_status_of_previous_user_scenarios():
        for user_scenario in UserPhishingScenario.objects.filter(
            status=UserSimulationStatus.IDLE,
            created_at__lt=timezone.now() - timedelta(days=2)
        ).iterator():
            user_scenario.status = UserSimulationStatus.PASSED_OR_IGNORED
            user_scenario.save()
