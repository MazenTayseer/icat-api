import factory

from apps.dal.models.user_assessment import (EssayAnswerSubmission,
                                             McqAnswerSubmission,
                                             UserAssessments)
from common.tests.factory.AnswerFactory import McqAnswerFactory
from common.tests.factory.AssessmentFactory import AssessmentFactory
from common.tests.factory.QuestionFactory import (EssayQuestionFactory,
                                                  McqQuestionFactory)
from common.tests.factory.UserFactory import UserFactory


class UserAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserAssessments

    user = factory.SubFactory(UserFactory)
    assessment = factory.SubFactory(AssessmentFactory)
    score = factory.Faker('pyfloat', left_digits=1, right_digits=1, positive=True, max_value=10)
    max_score = factory.Faker('pyfloat', left_digits=1, right_digits=1, positive=True, min_value=10, max_value=15)


class McqAnswerSubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = McqAnswerSubmission

    user_assessment = factory.SubFactory(UserAssessmentFactory)
    question = factory.SubFactory(McqQuestionFactory)
    answer = factory.SubFactory(McqAnswerFactory)
    score = factory.Faker('pyfloat', left_digits=1, right_digits=1, positive=True, max_value=1)
    max_score = 1.0


class EssayAnswerSubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EssayAnswerSubmission

    user_assessment = factory.SubFactory(UserAssessmentFactory)
    question = factory.SubFactory(EssayQuestionFactory)
    answer = factory.Faker('text', max_nb_chars=500)
    score = factory.Faker('pyfloat', left_digits=1, right_digits=1, positive=True, max_value=5)
    max_score = factory.Faker('pyfloat', left_digits=1, right_digits=1, positive=True, min_value=5, max_value=10)
