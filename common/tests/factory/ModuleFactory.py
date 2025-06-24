import factory

from apps.dal.models import Module


class ModuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Module

    name = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text', max_nb_chars=200)
    text = factory.Faker('text', max_nb_chars=300)
