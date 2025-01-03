from rest_framework import serializers
from .models import UserRestriction

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


# TODO
# @extend_schema_serializer(
#     examples = [
#          OpenApiExample(
#             'Example 0',
#             summary='UserRestrictionSerializer response example',
#             description='longer description',
#             value={
#                 'restriction_type': 0,
#                 'restriction_reason': "test",
#                 "api_response": "aaa",
#             },
#         ),
#     ]
# )
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
