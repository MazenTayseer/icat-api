import factory

from apps.dal.models import Assessment
from apps.dashboard.tests.factory.ModuleFactory import ModuleFactory


class AssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Assessment

    name = factory.Faker('sentence', nb_words=3)
    module = factory.SubFactory(ModuleFactory)
