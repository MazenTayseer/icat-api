from apps.dal.models.simulations.phishing_scenario import UserPhishingScenario
from common.tasks.tasks import send_phising_email
from common.tests.base import BaseTestCase
from common.tests.decorators import mock_phishing_clients
from common.tests.factory import PhishingScenarioFactory, UserFactory
from icat import celery_app


class SendPhishingEmailTaskTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        celery_app.conf.task_always_eager = True
        self.users_count = 2
        self.users = UserFactory.create_batch(self.users_count)
        self.scenario = PhishingScenarioFactory(
            tag="Banking Phishing",
            subject="Important Account Notice",
            seed="Test phishing scenario"
        )

    def tearDown(self):
        super().tearDown()
        celery_app.conf.task_always_eager = False

    @mock_phishing_clients
    def test_send_phising_email_creates_user_scenarios(
        self,
        mock_mailer_instance,
        mock_gemini_instance
    ):
        send_phising_email()
        self.assertEqual(mock_mailer_instance.send_email.call_count, self.users_count)
        self.assertEqual(mock_gemini_instance.chat.call_count, self.users_count)
        self.assertEqual(UserPhishingScenario.objects.count(), self.users_count)
