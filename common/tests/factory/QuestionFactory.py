import factory

from apps.dal.models import EssayQuestion, McqQuestion
from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dal.models.enums.initial_assessment_domain import \
    InitialAssessmentDomain
from common.tests.factory.AssessmentFactory import AssessmentFactory


class BaseQuestionFactory(factory.django.DjangoModelFactory):
    assessment = factory.SubFactory(AssessmentFactory)
    text = factory.Faker('text')
    difficulty = factory.Faker('random_int', min=1, max=5)

    @factory.lazy_attribute
    def domain(self):
        if self.assessment.type == AssessmentType.INITIAL:
            return InitialAssessmentDomain.AUTHENTICATION
        return None


class McqQuestionFactory(BaseQuestionFactory):
    class Meta:
        model = McqQuestion


class EssayQuestionFactory(BaseQuestionFactory):
    class Meta:
        model = EssayQuestion
