from django.db import models

from apps.dal.models.enums.user_simulation_status import UserSimulationStatus
from common.utils import generate_uuid


class Simulation(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    name = models.CharField(max_length=255, blank=False, null=False)
    module = models.ForeignKey(
        'Module',
        on_delete=models.CASCADE,
        related_name='simulations',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dal'

    def __str__(self):
        return self.name


class UserSimulation(models.Model):
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
    simulation = models.ForeignKey(
        'Simulation',
        on_delete=models.CASCADE,
        related_name='users',
    )
    status = models.CharField(
        choices=UserSimulationStatus.CHOICES,
        default=UserSimulationStatus.IN_PROGRESS,
        max_length=255,
        blank=False,
        null=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dal'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'simulation'],
                name='unique_user_simulation'
            )
        ]

    def __str__(self):
        return f'{self.user.email} - {self.simulation}'
