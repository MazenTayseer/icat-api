from django.core.exceptions import ValidationError
from django.db import models

from common.utils import generate_uuid


class BaseAnswer(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    text = models.TextField(blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = 'dal'

    def __str__(self):
        return self.text


class McqAnswer(BaseAnswer):
    question = models.ForeignKey(
        'McqQuestion',
        on_delete=models.CASCADE,
        related_name='answers',
    )
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_correct and McqAnswer.objects.filter(question=self.question, is_correct=True).exclude(id=self.id).exists():
            raise ValidationError("Only one answer can be correct per question")
        super().save(*args, **kwargs)


class EssayAnswerRubric(BaseAnswer):
    question = models.ForeignKey(
        'EssayQuestion',
        on_delete=models.CASCADE,
        related_name='rubric',
    )
    value = models.PositiveSmallIntegerField(blank=False, null=False)
    weight = models.FloatField(blank=False, null=False)
