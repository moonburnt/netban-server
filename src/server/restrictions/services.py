from django.db import transaction
from datetime import datetime
from typing import Any
from server.platform.models import PlatformUser, PlatformGroup
from .models import UserRestriction
from .choices import UserRestrictionType
from .exceptions import UnrestrictableUser, NotAnInstanceAdmin


def is_admin(platform_user: str | PlatformUser) -> bool:
    """Permission check to ensure the specified user has admin rights."""

    # Right now: if a platform user is tied to the server account - it is an admin.
    if isinstance(platform_user, PlatformUser):
        return hasattr(platform_user, "user")

    else:
        return bool(
            PlatformUser.objects.filter(
                identifier=platform_user,
                user__isnull=False,
            ).count()
        )


class UserRestrictionService:
    def __init__(
        self, user: str | PlatformUser, group: str | PlatformGroup | None = None
    ):
        if isinstance(user, PlatformUser):
            self._user = user
            self._user_identifier = user.identifier
        else:
            self._user_identifier = user
            self._user = PlatformUser.objects.filter(
                identifier=user,
            ).first()

        # If None - threat this instance as a netban instance, that works globally
        if (group is None) or isinstance(group, PlatformGroup):
            self._platform_group = group
        else:
            self._platform_group = PlatformGroup.objects.get_or_create(
                identifier=group,
            )[0]

    @property
    def user(self) -> PlatformUser:
        if not self._user:
            self._user = PlatformUser.objects.get_or_create(
                identifier=self._user_identifier,
            )[0]

        return self._user

    @property
    def group(self) -> PlatformGroup | None:
        return self._platform_group

    @transaction.atomic
    def restrict(
        self,
        restriction_type: UserRestrictionType,
        restricted_by: str | PlatformUser,
        length: datetime | None,
        reason: str | None,
    ) -> UserRestriction:
        """Add restriction to this user."""

        if self.is_global:
            if not is_admin(restricted_by):
                raise NotAnInstanceAdmin(
                    "Only instance admins can create global restrictions"
                )

        if isinstance(restricted_by, str):
            restricted_by = PlatformUser.objects.get_or_create(
                identifier=restricted_by,
            )[0]

        if restricted_by.pk == self.user.pk:
            raise UnrestrictableUser("Unable to restrict yourself")

        restriction = UserRestriction.objects.create(
            platform_user=self.user,
            platform_group=self.group,
            restricted_by=restricted_by,
            restriction_type=restriction_type,
            restriction_length=length,
            restriction_reason=reason,
        )

        # This is a bit awkward, but the object returned from create() will
        # not contain aggregated values, which we need to display in our response
        return UserRestriction.objects.get(pk=restriction.pk)

    def get_restrictions(
        self,
        by_type: UserRestrictionType | None = None,
    ) -> "Queryset[UserRestriction]":
        """Retrieve a list of currently active restrictions for user.

        Optionally filter by type.
        """

        qs_filter = dict(
            platform_user__identifier=self.user.identifier,
            is_active=True,
        )
        if by_type is not None:
            qs_filter["restriction_type"] = by_type

        if self.group is None:
            qs_filter["platform_group__isnull"] = True
        else:
            qs_filter["platform_group"] = self.group

        return UserRestriction.objects.filter(**qs_filter)

    @property
    def is_global(self) -> bool:
        """If False - this instance is group-specific, else - global."""

        return bool(self.group is None)
