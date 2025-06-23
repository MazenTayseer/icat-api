from setup import django_setup

django_setup()

from django.contrib.auth import get_user_model

from apps.dal.models.simulations.phishing_scenario import (
    PhishingScenario, UserPhishingScenario)
from apps.dal.models.simulations.simulation import Simulation
from common.clients.gemini_client import GeminiClient
from common.clients.mailer_client import MailerClient
from common.tasks.classes.phishing_simulator import PhishingSimulator


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
            user_scenario = UserPhishingScenario(
                user=user,
                phishing_scenario=scenario
            )
            email_body, subject = phishing_simulator.get_email_body_and_subject(scenario, user.first_name, user_scenario.id)
            phishing_simulator.run(
                email_body=email_body,
                subject=subject,
                recipient_email=user.email,
                scenario=scenario
            )

            objects_to_create.append(user_scenario)

        except Exception:
            # If the email fails, we don't want to block the whole task
            pass

    UserPhishingScenario.objects.bulk_create(objects_to_create)


if __name__ == "__main__":
    get_user_model().objects.all().delete()
    get_user_model().objects.create_user(
        email="mazen_tayseer@icloud.com",
        first_name="Mazen",
        last_name="Tayseer",
        password="Test1234",
        receive_emails=True,
    )
    simulation = Simulation.objects.create(
        name="Phishing"
    )
    PhishingScenario.objects.create(
        simulation=simulation,
        tag="VPN Reset",
        subject="URGENT: VPN password reset required",
        seed="""
        Write a professional phishing email that appears to come from the company
        IT help desk. Goal: make the user click a “Reset VPN Password” button
        today. Tone: polite urgency, reference security audit, use first name
        placeholder <<NAME>> in greeting. Return ONLY the raw HTML for the email
        body (120–160 words) with a single <b>Reset Now</b> button—no markdown or
        explanations.
        Return ONLY the HTML tags for the email body, with no explanation or markdown fence.
        """,
    )
    send_phising_email()
