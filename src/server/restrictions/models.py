from django.db import models
from django.utils.timezone import now
from .choices import UserRestrictionType
from .managers import UserRestrictionManager
from datetime import datetime


class UserRestriction(models.Model):
    platform_user = models.ForeignKey(
        to="platform.PlatformUser",
        related_name="restrictions",
        on_delete=models.CASCADE,
    )
    # If None - then its a netban, applicable for all platforms
    platform_group = models.ForeignKey(
        to="platform.PlatformGroup",
        related_name="restrictions",
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
    )
    restricted_by = models.ForeignKey(
        to="platform.PlatformUser",
        help_text=(
            "User who casted this restriction upon the platform_user.\n"
            "If unspecified - then its either a netban or initiator has deleted "
            "their account."
        ),
        related_name="created_restrictions",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )

    restriction_type = models.IntegerField(
        choices=UserRestrictionType.choices,
    )

    restriction_reason = models.TextField(
        blank=True,
        null=True,
        default=None,
    )

    restricted_since = models.DateTimeField(
        default=now,
    )
    restriction_length = models.DurationField(
        help_text=(
            "Specifies for how long this restriction applies. \n"
            "If unspecified - user is restricted permanently"
        ),
        blank=True,
        null=True,
        default=None,
    )

    objects = UserRestrictionManager()

    # restricted_until, is_active - are now parts of the manager
    def __str__(self) -> str:
        return f"{UserRestrictionType(self.restriction_type).name} of the @{self.platform_user.identifier}"
