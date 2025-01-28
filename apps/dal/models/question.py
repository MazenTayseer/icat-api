from django.db import models

from common.utils import generate_uuid


class Question(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    assessment = models.ForeignKey(
        'Assessment',
        on_delete=models.CASCADE,
        related_name='questions',
    )
    text = models.TextField(blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.update_assessment_max_score()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'dal'

    def __str__(self):
        return self.text

    def update_assessment_max_score(self):
        self.assessment.max_score += 1
        self.assessment.save()
