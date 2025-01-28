from django.conf import settings

from common.tests.base import BaseTestCase


class DashboardBaseTestCase(BaseTestCase):
    def setUp(self):
        self.dashboard_url = f"{settings.BASE_URL}/api/dashboard"
        super().setUp()
