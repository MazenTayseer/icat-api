from django.contrib.auth import get_user_model

from apps.dal.models.simulations.phishing_scenario import UserPhishingScenario
from common.clients.gemini_client import GeminiClient
from common.clients.mailer_client import MailerClient
from common.tasks.classes.phishing_simulator import PhishingSimulator
from icat import celery_app


@celery_app.task
def send_phising_email():
    objects_to_create = []
    mailer_client = MailerClient()
    gemini_client = GeminiClient()
    for user in get_user_model().objects.filter(is_superuser=False, receive_emails=True).iterator():
        try:
            phishing_simulator = PhishingSimulator(
                mailer_client=mailer_client,
                gemini_client=gemini_client
            )
            scenario = phishing_simulator.pick_scenario()
            email_body, subject = phishing_simulator.get_email_body_and_subject(scenario, user.first_name)
            phishing_simulator.run(
                email_body=email_body,
                subject=subject,
                recipient_email=user.email,
                scenario=scenario
            )

            objects_to_create.append(
                UserPhishingScenario(
                    user=user,
                    phishing_scenario=scenario,
                    email_body=email_body,
                    subject=subject
                )
            )
        except Exception:
            # If the email fails, we don't want to block the whole task
            pass

    UserPhishingScenario.objects.bulk_create(objects_to_create)
