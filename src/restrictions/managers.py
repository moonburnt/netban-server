from django.db.models import (
    Manager,
    Q,
    Case,
    When,
    F,
    DateTimeField,
    Sum,
    DurationField,
    Func,
    ExpressionWrapper,
)
from django.utils.timezone import now
from datetime import datetime


class UserRestrictionManager(Manager):
    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.annotate(
            restricted_until=Case(
                When(
                    restriction_length__isnull=False,
                    then=F("restricted_since") + F("restriction_length"),
                ),
                output_field=DurationField(),
            )
        )
        qs = qs.annotate(
            is_active=Q(
                Q(restricted_until__isnull=True)
                | Q(restricted_until__gt=now()),
            )
        )

        return qs
