from django.db import models

from apps.dal.models.enums.user_simulation_status import UserSimulationStatus
from common.utils import generate_uuid


class PhishingScenario(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    simulation = models.ForeignKey(
        'Simulation',
        on_delete=models.CASCADE,
        related_name='simulations',
    )
    tag = models.CharField(max_length=255, blank=False, null=False)
    subject = models.CharField(max_length=255, blank=False, null=False)
    seed = models.TextField(blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dal'

    def __str__(self):
        return self.tag


class UserPhishingScenario(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    user = models.ForeignKey(
        'custom_auth.User',
        on_delete=models.CASCADE,
        related_name='simulations'
    )
    phishing_scenario = models.ForeignKey(
        'PhishingScenario',
        on_delete=models.CASCADE,
        related_name='users',
    )
    status = models.CharField(
        choices=UserSimulationStatus.CHOICES,
        default=UserSimulationStatus.IDLE,
        max_length=255,
        blank=False,
        null=False
    )
    email_body = models.TextField()
    subject = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dal'

    def __str__(self):
        return f'{self.user.email} - {self.phishing_scenario.tag}'
