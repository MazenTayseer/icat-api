import factory

from apps.dal.models import Simulation


class SimulationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Simulation

    name = factory.Faker('company')
