from django.db import models
from django.contrib.auth.models import AbstractUser
from . import constants


class PlatformUser(models.Model):
    """Platform specific user data.

    Restricted users only have this, admins may tie this to their account.
    """

    identifier = models.CharField(
        max_length=constants.USER_IDENTIFIER_LENGTH,
        unique=True,
    )

    # TODO: maybe add "platform" field for the potential support of other
    # platforms besides TG?

    def __str__(self) -> str:
        return self.identifier


class PlatformGroup(models.Model):
    """Platform specific group data."""

    identifier = models.CharField(
        max_length=constants.GROUP_IDENTIFIER_LENGTH,
        unique=True,
    )

    def __str__(self) -> str:
        return self.identifier
