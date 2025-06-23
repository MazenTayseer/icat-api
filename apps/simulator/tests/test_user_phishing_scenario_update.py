from rest_framework import status

from apps.dal.models.enums.user_simulation_status import UserSimulationStatus
from apps.simulator.tests.base import SimulatorBaseTestCase
from common.tests.factory import UserFactory, UserPhishingScenarioFactory


class UserPhishingScenarioUpdateViewTestCase(SimulatorBaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_phishing_scenario = UserPhishingScenarioFactory(
            user=self.user,
            status=UserSimulationStatus.IDLE
        )
        self.other_user = UserFactory(email="other@test.com")
        self.other_user_scenario = UserPhishingScenarioFactory(
            user=self.other_user,
            status=UserSimulationStatus.IDLE
        )

    def test_update_user_phishing_scenario_success(self):
        url = f"{self.simulator_url}/{self.user_phishing_scenario.id}/update/"

        response = self.send_unauth_request("patch", url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user_phishing_scenario.refresh_from_db()
        self.assertEqual(self.user_phishing_scenario.status, UserSimulationStatus.FAILED)
        self.assertEqual(response.data['detail'], "UserPhishingScenario status updated successfully.")

    def test_update_user_phishing_scenario_not_idle(self):
        self.user_phishing_scenario.status = UserSimulationStatus.PASSED_OR_IGNORED
        self.user_phishing_scenario.save()

        url = f"{self.simulator_url}/{self.user_phishing_scenario.id}/update/"

        response = self.send_unauth_request("patch", url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
