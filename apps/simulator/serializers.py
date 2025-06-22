from rest_framework import serializers

from apps.dal.models.enums.user_simulation_status import UserSimulationStatus
from apps.dal.models.simulations.phishing_scenario import UserPhishingScenario


class UserPhishingScenarioUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=UserSimulationStatus.CHOICES,
        required=True
    )

    class Meta:
        model = UserPhishingScenario
        fields = ['status']
        read_only_fields = ['id', 'created_at', 'updated_at']
