from django.contrib.auth import get_user_model

from apps.dal.models.simulations.phishing_scenario import UserPhishingScenario
from common.clients.mailer_client import MailerClient
from common.clients.ollama_client import OllamaClient
from common.tasks.classes.phishing_simulator import PhishingSimulator
from icat import celery_app


@celery_app.task
def send_phising_email():
    objects_to_create = []
    for user in get_user_model().objects.filter(is_superuser=False).iterator():
        mailer_client = MailerClient()
        ollama_client = OllamaClient()

        phishing_simulator = PhishingSimulator(
            mailer_client=mailer_client,
            ollama_client=ollama_client
        )
        scenario = phishing_simulator.pick_scenario()
        phishing_simulator.run(
            first_name=user.first_name,
            recipient_email=user.email,
            scenario=scenario
        )

        objects_to_create.append(
            UserPhishingScenario(
                user=user,
                phishing_scenario=scenario
            )
        )

    UserPhishingScenario.objects.bulk_create(objects_to_create)
