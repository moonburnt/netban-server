from django.db import models
from django.contrib.auth.models import AbstractUser


class PlatformUser(models.Model):
    """Platform specific user data.

    Restricted users only have this, admins may tie this to their account.
    """

    user_id = models.CharField(
        max_length=128,
        unique=True,
    )

    # TODO: maybe add "platform" field for the potential support of other
    # platforms besides TG?

    def __str__(self) -> str:
        return self.user_id


class User(AbstractUser):
    # Optional ability to specify which platform id belongs to this admin account.
    # May be used for other purposes in future
    platform_user = models.OneToOneField(
        to=PlatformUser,
        related_name="user",
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
    )
