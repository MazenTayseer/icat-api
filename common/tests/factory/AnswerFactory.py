import factory

from apps.dal.models import Answer
from common.tests.factory.QuestionFactory import QuestionFactory


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    question = factory.SubFactory(QuestionFactory)
    text = factory.Faker('text')
    is_correct = False
