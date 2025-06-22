from common.tests.base import BaseTestCase


class SimulatorBaseTestCase(BaseTestCase):
    def setUp(self):
        self.simulator_url = "/api/simulator"
        super().setUp()
