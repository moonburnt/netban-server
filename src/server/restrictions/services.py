from django.db import transaction
from datetime import datetime
from typing import Any
from server.platform.models import PlatformUser, PlatformGroup
from .models import UserRestriction
from .choices import UserRestrictionType
from .exceptions import UnrestrictableUser


class UserRestrictionService:
    def __init__(
        self, user: str | PlatformUser, group: str | PlatformGroup | None = None
    ):
        if isinstance(user, PlatformUser):
            self._platform_user = user
            self._identifier = user.pk
        else:
            self._identifier = user
            self._platform_user = PlatformUser.objects.filter(
                identifier=user,
            ).first()

        # If None - threat this instance as a netban instance, that works globally
        if isinstance(group, (PlatformGroup, None)):
            self._platform_group = group
        else:
            self._platform_group = PlatformGroup.objects.get_or_create(
                identifier=group,
            )[0]

    @transaction.atomic
    def restrict(
        self,
        restriction_type: UserRestrictionType,
        length: datetime | None,
        reason: str | None,
    ) -> UserRestriction:
        """Add restriction to this user."""

        if not self._platform_user:
            self._platform_user = PlatformUser.objects.get_or_create(
                identifier=self._identifier,
            )[0]

        restriction = UserRestriction.objects.create(
            platform_user=self._platform_user,
            platform_group=self._platform_group,
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
            platform_user__identifier=self._identifier,
            is_active=True,
        )
        if by_type is not None:
            qs_filter["restriction_type"] = by_type

        if self._platform_group is None:
            qs_filter["restriction_group__isnull"] = True
        else:
            qs_filter["restriction_group"] = self._platform_group

        return UserRestriction.objects.filter(**qs_filter)

    @property
    def is_group_specific(self) -> bool:
        """If True - this instance is group-specific, else - global."""

        return bool(self._platform_group is not None)
