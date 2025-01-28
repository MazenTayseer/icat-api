import factory

from apps.dal.models import Question
from apps.dashboard.tests.factory.AssessmentFactory import AssessmentFactory


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    assessment = factory.SubFactory(AssessmentFactory)
    text = factory.Faker('text')
