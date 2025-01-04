from django.db import models
from django.contrib.auth.models import AbstractUser


class PlatformUser(models.Model):
    """Platform specific user data.

    Restricted users only have this, admins may tie this to their account.
    """

    identifier = models.CharField(
        max_length=128,
        unique=True,
    )

    # TODO: maybe add "platform" field for the potential support of other
    # platforms besides TG?

    def __str__(self) -> str:
        return self.identifier


class PlatformGroup(models.Model):
    """Platform specific group data."""

    identifier = models.CharField(
        max_length=128,
        unique=True,
    )

    def __str__(self) -> str:
        return self.identifier
