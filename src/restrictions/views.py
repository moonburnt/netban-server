from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from .serializers import UserRestrictionSerializer
from .models import UserRestriction


class UserRestrictionView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UserRestriction.objects.filter(is_active=True)
    serializer_class = UserRestrictionSerializer
    permission_classes = (permissions.AllowAny,)  # TODO: token-based auth

    def get_queryset(self):
        user = self.request.GET.get("user", None)
        if not user:
            raise ValidationError("'user' is required")

        return super().get_queryset().filter(platform_user__user_id=user)

    @extend_schema(
        tags=("restriction",),
        parameters=[
            OpenApiParameter(
                name="user",
                type=str,
                required=True,
            )
        ],
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)
