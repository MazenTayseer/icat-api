from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.dal.models.enums.user_simulation_status import UserSimulationStatus
from apps.dal.models.simulations.phishing_scenario import UserPhishingScenario
from apps.simulator.serializers import UserPhishingScenarioUpdateSerializer


class UserPhishingScenarioUpdateView(APIView):
    def patch(self, request, scenario_id, *args, **kwargs):
        try:
            user_phishing_scenario = UserPhishingScenario.objects.get(id=scenario_id)
        except UserPhishingScenario.DoesNotExist:
            return Response(
                {"detail": "UserPhishingScenario not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if user_phishing_scenario.status != UserSimulationStatus.IDLE:
            return Response(
                {"detail": "UserPhishingScenario is not in IDLE status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserPhishingScenarioUpdateSerializer(
            user_phishing_scenario,
            data={"status": UserSimulationStatus.FAILED},
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "UserPhishingScenario status updated successfully."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
