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

    @property
    def max_score(self):
        return sum(question.max_score for question in self.questions)


class UserAssessments(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    user = models.ForeignKey(
        'custom_auth.User',
        on_delete=models.CASCADE,
        related_name='assessments'
    )
    assessment = models.ForeignKey(
        'Assessment',
        on_delete=models.CASCADE,
        related_name='users',
    )
    score = models.FloatField(blank=False, null=False)
    trial = models.PositiveIntegerField(blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.trial:
            self.trial = UserAssessments.objects.filter(user=self.user, assessment=self.assessment).count() + 1
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'dal'
        unique_together = ('user', 'assessment', 'trial')

    def __str__(self):
        return f"{self.user.email} - {self.assessment.name} - {self.score}"

    @property
    def is_passed(self):
        return self.score_percentage >= 50

    @property
    def score_percentage(self):
        return (self.score / self.assessment.max_score) * 100
