from django.conf import settings

from common.tests.base import BaseTestCase


class CustomAuthBaseTestCase(BaseTestCase):
    def setUp(self):
        self.custom_auth_url = f"{settings.BASE_URL}/api/auth"
        super().setUp()
