from django.db import models

from common.utils import generate_uuid


class Leaderboard(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dal'

    def __str__(self):
        return self.name


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
            self.__class__.objects
            .filter(leaderboard=self.leaderboard, total_score__gt=self.total_score)
            .count() + 1
        )
