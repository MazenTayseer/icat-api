from django.db import models

from common.utils import generate_uuid


class Leaderboard(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    user = models.ForeignKey(
        'custom_auth.User',
        on_delete=models.CASCADE,
        related_name='leaderboard'
    )
    total_score = models.IntegerField(default=0, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'dal'
        ordering = ['-total_score']
        
    def __str__(self):
        return f"{self.user.email} - {self.total_score}"
    
    @property
    def get_position(self):
        return Leaderboard.objects.filter(total_score__gt=self.total_score).count() + 1