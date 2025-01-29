from django.db import models

from common.utils import generate_uuid


class Assessment(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    name = models.CharField(max_length=255, blank=False, null=False)
    max_score = models.IntegerField(default=0)
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

    def __str__(self):
        return self.name


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
    score_percentage = models.FloatField(blank=False, null=False)
    is_passed = models.BooleanField(blank=False, null=False)
    trial = models.PositiveIntegerField(blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.trial:
            self.trial = UserAssessments.objects.filter(user=self.user, assessment=self.assessment).count() + 1
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'dal'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'assessment', 'trial'],
                name='unique_user_assessment_trial'
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.assessment.name} - {self.score}"
