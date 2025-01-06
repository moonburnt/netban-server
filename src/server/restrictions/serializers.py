from rest_framework import serializers
from .models import UserRestriction
from .choices import UserRestrictionType

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Request Example 0",
            summary="A daily ban example",
            response_only=True,
            value={
                "restriction_type": UserRestrictionType.BAN,
                "restriction_reason": "Was bad",
                "restricted_since": "2025-01-04T01:23:23.240899Z",
                "restricted_until": "2025-01-05T01:23:23.240899Z",
            },
        ),
        OpenApiExample(
            "Request Example 1",
            summary="A permanent ban example",
            response_only=True,
            value={
                "restriction_type": UserRestrictionType.BAN,
                "restriction_reason": "Was bad",
                "restricted_since": "2025-01-04T01:23:23.240899Z",
                "restricted_until": None,
            },
        ),
    ]
)
class UserRestrictionSerializer(serializers.ModelSerializer):
    restricted_until = serializers.DateTimeField()

    class Meta:
        model = UserRestriction
        fields = (
            "restriction_type",
            "restriction_reason",
            "restricted_since",
            "restricted_until",
        )


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Request Example 0",
            summary="Example",
            description=(
                # TODO: description for other fields
                "- user: user id on the platform, no longer than 128 symbols.\n"
                "- restriction_length: length of the restiction in HH:MM:SS fmt.\n"
            ),
            request_only=True,
            value={
                "user": "123",
                "restriction_type": UserRestrictionType.BAN,
                "restriction_reason": "Was bad",
                "restriction_length": "10:12:00",
            },
        ),
    ]
)
class UserRestrictionRestrictSerializer(serializers.Serializer):
    # Max length from PlatformUser.identifer
    user = serializers.CharField(
        max_length=128,
        required=True,
    )
    # Max length from PlatformGroup.identifier
    group = serializers.CharField(
        max_length=128,
        required=False,
    )

    restriction_type = serializers.ChoiceField(
        choices=UserRestrictionType,
        required=True,
    )
    restriction_reason = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    restriction_length = serializers.DurationField(
        required=False,
        help_text="If not set - will be forever",
    )
