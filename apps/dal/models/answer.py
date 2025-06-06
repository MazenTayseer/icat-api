from django.db import models

from common.utils import generate_uuid


class Answer(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='answers',
    )
    text = models.TextField(blank=False, null=False)
    is_correct = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dal'

    def save(self, *args, **kwargs):
        if self.is_correct and Answer.objects.filter(question=self.question, is_correct=True).exclude(id=self.id).exists():
            raise ValueError("Only one answer can be correct per question")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text
