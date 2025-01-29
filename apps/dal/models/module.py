from django.db import models

from common.utils import generate_uuid


class Module(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    text = models.JSONField(blank=False, null=False, default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dal'

    def __str__(self):
        return self.name


class UserModule(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    user = models.ForeignKey(
        'custom_auth.User',
        on_delete=models.CASCADE,
        related_name='modules'
    )
    module = models.ForeignKey(
        'Module',
        on_delete=models.CASCADE,
        related_name='users',
    )
    completion_percentage = models.FloatField(blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dal'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'module'],
                name='unique_user_module'
            )
        ]

    def __str__(self):
        return f'{self.user.email} - {self.module}'
