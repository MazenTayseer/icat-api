from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.custom_auth.enums.experience_levels import ExperienceLevels
from apps.custom_auth.user_manager import CustomUserManager
from common.utils import generate_uuid


class User(AbstractUser):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        default=generate_uuid,
    )
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)
    
    experience_level = models.CharField(
        choices=ExperienceLevels.CHOICES,
        default=ExperienceLevels.BEGINNER,
        max_length=255,
        blank=False,
        null=False
    )
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        app_label = 'custom_auth'
    
    def __str__(self):
        return self.email