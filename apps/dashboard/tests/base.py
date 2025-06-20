
from common.tests.base import BaseTestCase


class DashboardBaseTestCase(BaseTestCase):
    def setUp(self):
        self.dashboard_url = "/api/dashboard"
        super().setUp()
