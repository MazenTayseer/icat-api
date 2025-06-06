from django.conf import settings

from apps.dal.models import PhishingScenario
from common.clients.mailer_client import MailerClient
from common.clients.ollama_client import OllamaClient


class PhishingSimulator:
    def __init__(self, ollama_client: OllamaClient, mailer_client: MailerClient):
        self.ollama_client = ollama_client
        self.mailer_client = mailer_client
        self.email_template = "common/emails/phishing.html"

    def __render_email_body(self, seed: str, first_name: str):
        rsp = self.ollama_client.chat(
            model=settings.OLLAMA_MODEL,
            messages=[{"role": "user", "content": seed}],
            stream=False
        )
        return rsp["message"]["content"]

    def __format_email_body(self, email_body: str, first_name: str):
        email_body = email_body.replace("<<NAME>>", first_name)
        return email_body

    def __format_email_subject(self, subject: str, first_name: str):
        subject = subject.replace("<<NAME>>", first_name)
        return subject

    def pick_scenario(self):
        return PhishingScenario.objects.order_by('?').first()

    def run(
        self,
        first_name: str,
        recipient_email: str,
        scenario: PhishingScenario
    ):
        email_body = self.__render_email_body(scenario.seed, first_name)
        email_body = self.__format_email_body(email_body, first_name)
        subject = self.__format_email_subject(scenario.subject, first_name)
        self.mailer_client.send_email(
            email_template=self.email_template,
            subject=subject,
            message=email_body,
            to=recipient_email
        )
