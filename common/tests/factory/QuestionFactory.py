import factory

from apps.dal.models import EssayQuestion, McqQuestion
from common.tests.factory.AssessmentFactory import AssessmentFactory


class BaseQuestionFactory(factory.django.DjangoModelFactory):
    assessment = factory.SubFactory(AssessmentFactory)
    text = factory.Faker('text')
    difficulty = factory.Faker('random_int', min=1, max=5)
    domain = None


class McqQuestionFactory(BaseQuestionFactory):
    class Meta:
        model = McqQuestion


class EssayQuestionFactory(BaseQuestionFactory):
    class Meta:
        model = EssayQuestion
