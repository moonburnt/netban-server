from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Optional ability to specify which platform id belongs to this admin account.
    # May be used for other purposes in future
    platform_user = models.OneToOneField(
        to="platform.PlatformUser",
        related_name="user",
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
    )
