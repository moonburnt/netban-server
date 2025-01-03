from django.db import transaction
from datetime import datetime
from typing import Any
from users.models import PlatformUser
from .models import UserRestriction
from .choices import UserRestrictionType
from .exceptions import UnrestrictableUser


class UserRestrictionService:
    def __init__(self, user: str | PlatformUser):
        if isinstance(user, PlatformUser):
            self._platform_user = user
            self._user_id = user.pk
        else:
            self._user_id = user
            self._platform_user = PlatformUser.objects.filter(
                user_id=user,
            ).first()

    @transaction.atomic
    def restrict(
        self,
        restriction_type: UserRestrictionType,
        length: datetime | None,
        reason: str | None,
    ) -> UserRestriction:
        if not self._platform_user:
            self._platform_user = PlatformUser.objects.get_or_create(
                user_id=self._user_id,
            )[0]

        return UserRestriction.objects.create(
            platform_user=self._platform_user,
            restriction_type=restriction_type,
            restriction_length=length,
            restriction_reason=reason,
        )

    def get_restrictions(
        self,
        by_type: UserRestrictionType | None = None,
    ) -> "Queryset[UserRestriction]":
        qs_filter = dict(
            platform_user__pk=self._user_id,
            is_active=True,
        )
        if by_type is not None:
            qs_filter["restriction_type"] = by_type

        return UserRestriction.objects.filter(**qs_filter)
