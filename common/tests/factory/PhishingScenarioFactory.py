import factory

from apps.dal.models import PhishingScenario
from common.tests.factory.SimulationFactory import SimulationFactory


class PhishingScenarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PhishingScenario

    simulation = factory.SubFactory(SimulationFactory)
    tag = factory.Faker('word')
    subject = factory.Faker('sentence', nb_words=4)
    seed = factory.Faker('text', max_nb_chars=500)
