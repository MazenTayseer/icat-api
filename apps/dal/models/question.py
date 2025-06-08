from django.core.exceptions import ValidationError
from django.db import models

from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dal.models.enums.initial_assessment_domain import \
    InitialAssessmentDomain
from common.utils import generate_uuid


class BaseQuestion(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    assessment = models.ForeignKey(
        'Assessment',
        on_delete=models.CASCADE,
        db_index=True,
    )
    domain = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=InitialAssessmentDomain.choices,
    )
    difficulty = models.PositiveSmallIntegerField()
    text = models.TextField(blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.assessment.type == AssessmentType.INITIAL and not self.domain:
            raise ValidationError("Initial assessment questions must have a domain")
        if self.assessment.type == AssessmentType.MODULE and self.domain:
            raise ValidationError("Module assessment questions cannot have a domain")
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'dal'

    def __str__(self):
        return self.stem


class McqQuestion(BaseQuestion):
    assessment = models.ForeignKey(
        'Assessment',
        on_delete=models.CASCADE,
        related_name='mcq_questions',
        db_index=True,
    )

    @property
    def max_score(self):
        return 1

class EssayQuestion(BaseQuestion):
    assessment = models.ForeignKey(
        'Assessment',
        on_delete=models.CASCADE,
        related_name='essay_questions',
        db_index=True,
    )

    @property
    def max_score(self):
        return sum(rubric.value for rubric in self.rubric.all())
