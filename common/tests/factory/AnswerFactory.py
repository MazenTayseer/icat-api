import factory

from apps.dal.models import EssayAnswerRubric, McqAnswer
from common.tests.factory.QuestionFactory import (EssayQuestionFactory,
                                                  McqQuestionFactory)


class McqAnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = McqAnswer

    question = factory.SubFactory(McqQuestionFactory)
    text = factory.Faker('text')
    is_correct = False


class EssayAnswerRubricFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EssayAnswerRubric

    question = factory.SubFactory(EssayQuestionFactory)
    value = factory.Faker('random_int', min=1, max=10)
    text = factory.Faker('text')
    weight = factory.Faker('pyfloat', left_digits=1, right_digits=2, positive=True, min_value=0.1, max_value=1.0)
