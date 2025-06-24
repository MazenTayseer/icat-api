from django.db import models

from apps.dal.models.enums.assessment_type import AssessmentType
from apps.dal.models.enums.leaderboard_type import LeaderboardType
from common.utils import generate_uuid


class Leaderboard(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    type = models.CharField(
        max_length=255,
        choices=LeaderboardType.choices,
        default=LeaderboardType.GLOBAL,
        unique=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dal'

    def __str__(self):
        return self.type


class LeaderboardEntry(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    leaderboard = models.ForeignKey(
        'Leaderboard',
        on_delete=models.CASCADE,
        related_name='entries'
    )
    user = models.ForeignKey(
        'custom_auth.User',
        on_delete=models.CASCADE,
        related_name='leaderboard_entry'
    )
    total_score = models.IntegerField(default=0, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dal'
        ordering = ['-total_score']
        unique_together = ('leaderboard', 'user')

    def __str__(self):
        return f"{self.user.email} - {self.total_score}"

    @property
    def position(self):
        return (
            LeaderboardEntry.objects
            .filter(leaderboard=self.leaderboard, total_score__gt=self.total_score)
            .count() + 1
        )

    @property
    def modules_completed(self):
        return len(set(
            ua.assessment.id for ua in self.user.assessments.all()
            if ua.assessment.type == AssessmentType.MODULE and ua.is_passed
        ))
