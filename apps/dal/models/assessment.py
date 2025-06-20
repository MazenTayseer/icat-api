from itertools import chain

from django.core.exceptions import ValidationError
from django.db import models

from apps.dal.models.enums.assessment_type import AssessmentType
from common.utils import generate_uuid


class Assessment(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    name = models.CharField(max_length=255, blank=False, null=False)
    type = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        choices=AssessmentType.choices,
        default=AssessmentType.INITIAL
    )
    module = models.ForeignKey(
        'Module',
        on_delete=models.CASCADE,
        related_name='assessments',
        blank=True,
        null=True,
    )
    max_questions_at_once = models.PositiveIntegerField(default=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dal'

    def save(self, *args, **kwargs):
        if self.type == AssessmentType.INITIAL and self.module:
            raise ValidationError("Initial assessment cannot have a module")
        if self.type == AssessmentType.MODULE and not self.module:
            raise ValidationError("Module assessment must have a module")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def questions(self):
        return chain(self.mcq_questions.all(), self.essay_questions.all())
