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

    # TODO: banned by (admin user for netbans or user id for local bans)

    # restricted_until, is_active - are now parts of the manager
    def __str__(self) -> str:
        return f"{UserRestrictionType(self.restriction_type).name} of the @{self.platform_user.identifier}"
