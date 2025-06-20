from itertools import chain

from django.db import models

from common.utils import generate_uuid


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
    max_score = models.FloatField(blank=False, null=False)
    trial = models.PositiveIntegerField(blank=False, null=False)
    feedback = models.TextField(blank=True, null=True)

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
        return self.percentage >= 50

    @property
    def percentage(self):
        return (self.score / self.max_score) * 100

    @property
    def answers(self):
        return chain(self.mcq_answers.all(), self.essay_answers.all())


class BaseUserAssessmentAnswer(models.Model):
    id = models.CharField(primary_key=True, max_length=255, default=generate_uuid)
    user_assessment = models.ForeignKey('UserAssessments', on_delete=models.CASCADE)
    score = models.FloatField(blank=False, null=False)
    max_score = models.FloatField(blank=False, null=False)
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = 'dal'

class McqAnswerSubmission(BaseUserAssessmentAnswer):
    user_assessment = models.ForeignKey('UserAssessments', on_delete=models.CASCADE, related_name='mcq_answers')
    question = models.ForeignKey('McqQuestion', on_delete=models.CASCADE)
    answer = models.ForeignKey('McqAnswer', on_delete=models.CASCADE)

    class Meta(BaseUserAssessmentAnswer.Meta):
        unique_together = ('user_assessment', 'question')

class EssayAnswerSubmission(BaseUserAssessmentAnswer):
    user_assessment = models.ForeignKey('UserAssessments', on_delete=models.CASCADE, related_name='essay_answers')
    question = models.ForeignKey('EssayQuestion', on_delete=models.CASCADE)
    answer = models.TextField()

    class Meta(BaseUserAssessmentAnswer.Meta):
        unique_together = ('user_assessment', 'question')
