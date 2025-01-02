from rest_framework import serializers
from .models import UserRestriction


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
