
from apps.dal.models import PhishingScenario
from apps.dal.models.enums.ai_roles import AIRole
from common.clients.gemini_client import GeminiClient, GeminiMessage
from common.clients.mailer_client import MailerClient
from common.prompts import Prompts


class PhishingSimulator:
    def __init__(self, gemini_client: GeminiClient, mailer_client: MailerClient):
        self.gemini_client = gemini_client
        self.mailer_client = mailer_client
        self.email_template = "common/emails/phishing.html"

    def __render_email_body(self, seed: str):
        return self.gemini_client.chat(
            system_message=GeminiMessage(role=AIRole.SYSTEM, content=Prompts.PHISHING_SIMULATOR_PROMPT),
            user_message=GeminiMessage(role=AIRole.USER, content=seed)
        )

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
        email_body = self.__render_email_body(scenario.seed)
        email_body = self.__format_email_body(email_body, first_name)
        subject = self.__format_email_subject(scenario.subject, first_name)
        self.mailer_client.send_email(
            email_template=self.email_template,
            subject=subject,
            message=email_body,
            to=recipient_email
        )
