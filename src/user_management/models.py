import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

from user_management.manager import CustomUserManager
from user_management.utils import UserTypeChoice

class CustomUser(AbstractUser):
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w @.+-]+$',
            message="Username may contain letters, numbers, spaces, and @/./+/-/_ characters.",
        )],
    )
    user_type = models.CharField(
        max_length=10,
        choices=UserTypeChoice.choices,
        default=UserTypeChoice.CARRIER,
        null=True,
        blank=True
    )
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_uploads/', default='profile_uploads/default_user.png')
    vehicle_type = models.CharField(max_length=50, null=True, blank=True)
    vehicle_capacity_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    base_rate_per_km = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Preferred rate per km for carriers")
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserStamp(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_creator"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_updater",
    )

    class Meta:
        abstract = True

class TimeStamp(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
