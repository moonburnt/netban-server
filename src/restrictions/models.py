from django.db import models
from django.utils.timezone import now
from .choices import UserRestrictionType
from .managers import UserRestrictionManager
from datetime import datetime


class UserRestriction(models.Model):
    platform_user = models.ForeignKey(
        to="users.PlatformUser",
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

    # @property
    # def restricted_until(self) -> datetime | None:
    #     # Only use together with is_active, since this may be None for both
    #     # infinite restriction and inactive restriction
    #     if self.restriction_length:
    #         return self.restricted_since + self.restriction_length
    #     else:
    #         return None

    # # TODO: add this to manager
    # @property
    # def is_active(self) -> bool:
    #     return bool(self.restricted_until and self.restricted_until < now())
