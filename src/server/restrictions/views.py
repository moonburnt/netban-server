from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import views, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from .serializers import (
    UserRestrictionSerializer,
    UserRestrictionRestrictSerializer,
)
from .services import UserRestrictionService


class UserRestrictionListView(views.APIView):
    # TODO: token-based auth

    @extend_schema(
        tags=("restriction",),
        parameters=[
            OpenApiParameter(
                name="user",
                type=str,
                required=True,
            ),
            OpenApiParameter(
                name="group",
                type=str,
                required=False,
            ),
        ],
        responses={
            200: UserRestrictionSerializer(many=True),
        },
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = request.GET.get("user", None)
        if not user:
            raise ValidationError("'user' is required")

        group = request.GET.get("group", None)

        service = UserRestrictionService(
            user=user,
            group=group,
        )
        restrictions = service.get_restrictions()

        # TODO: maybe paginate this or only return the most recent bans?
        return Response(
            data=UserRestrictionSerializer(restrictions, many=True).data,
            status=status.HTTP_200_OK,
        )


class UserRestrictionRestrictView(views.APIView):
    # TODO: token-based auth

    @extend_schema(
        tags=("restriction",),
        request=UserRestrictionRestrictSerializer,
        responses={
            200: UserRestrictionSerializer(many=False),
        },
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = UserRestrictionRestrictSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        # TODO: require request to be sent by an admin-related account for netbans
        service = UserRestrictionService(
            user=serializer.validated_data["user"],
            group=serializer.validated_data.get("group", None),
        )
        restriction = service.restrict(
            restriction_type=serializer.validated_data["restriction_type"],
            reason=serializer.validated_data["restriction_reason"],
            length=serializer.validated_data.get("restriction_length", None),
        )

        return Response(
            data=UserRestrictionSerializer(restriction).data,
            status=status.HTTP_200_OK,
        )
