import factory

from apps.dal.models.enums.user_simulation_status import UserSimulationStatus
from apps.dal.models.simulations.phishing_scenario import UserPhishingScenario
from common.tests.factory.PhishingScenarioFactory import \
    PhishingScenarioFactory
from common.tests.factory.UserFactory import UserFactory


class UserPhishingScenarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserPhishingScenario

    user = factory.SubFactory(UserFactory)
    phishing_scenario = factory.SubFactory(PhishingScenarioFactory)
    status = UserSimulationStatus.IDLE
    email_body = factory.Faker('text', max_nb_chars=200)
    subject = factory.Faker('sentence', nb_words=4)
