from django.db import models

from common.utils import generate_uuid


class Module(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dal'

    def __str__(self):
        return self.name
