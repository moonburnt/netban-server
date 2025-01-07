from rest_framework import serializers
from .models import UserRestriction
from .choices import UserRestrictionType
from server.platform import constants

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Request Example 0",
            summary="A daily ban example",
            response_only=True,
            value={
                "restriction_type": UserRestrictionType.BAN,
                "restricted_by": "5429",
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
                "restricted_by": "5429",
                "restriction_reason": "Was bad",
                "restricted_since": "2025-01-04T01:23:23.240899Z",
                "restricted_until": None,
            },
        ),
    ]
)
class UserRestrictionSerializer(serializers.ModelSerializer):
    restricted_until = serializers.DateTimeField()
    restricted_by = serializers.CharField(
        source="restricted_by.identifier",
        default=None,
    )

    class Meta:
        model = UserRestriction
        fields = (
            "restriction_type",
            "restricted_by",
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
                f"- user: user id on the platform, no longer than {constants.USER_IDENTIFIER_LENGTH} symbols.\n"
                f"- group: group id on the platform, no longer than {constants.GROUP_IDENTIFIER_LENGTH} symbols.\n"
                "- restriction_length: length of the restiction in HH:MM:SS fmt.\n"
            ),
            request_only=True,
            value={
                "user": "1234",
                "restricted_by": "5429",
                "group": "1629",
                "restriction_type": UserRestrictionType.BAN,
                "restriction_reason": "Was bad",
                "restriction_length": "10:12:00",
            },
        ),
    ]
)
class UserRestrictionRestrictSerializer(serializers.Serializer):
    user = serializers.CharField(
        max_length=constants.USER_IDENTIFIER_LENGTH,
        required=True,
    )
    restricted_by = serializers.CharField(
        max_length=constants.USER_IDENTIFIER_LENGTH,
        required=True,
    )
    group = serializers.CharField(
        max_length=constants.GROUP_IDENTIFIER_LENGTH,
        required=False,
        help_text="If not set - counts as a netban, additional checks will apply",
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
