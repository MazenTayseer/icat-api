
from common.tests.base import BaseTestCase


class CustomAuthBaseTestCase(BaseTestCase):
    def setUp(self):
        self.custom_auth_url = "/api/auth"
        super().setUp()
