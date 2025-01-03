from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import views, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from .serializers import UserRestrictionSerializer
from .services import UserRestrictionService


class UserRestrictionView(views.APIView):
    # TODO: token-based auth

    @extend_schema(
        tags=("restriction",),
        parameters=[
            OpenApiParameter(
                name="user",
                type=str,
                required=True,
            )
        ],
        responses={
            200: UserRestrictionSerializer(many=True),
        },
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = request.GET.get("user", None)
        if not user:
            raise ValidationError("'user' is required")

        service = UserRestrictionService(user=user)
        restrictions = service.get_restrictions()

        return Response(
            data=UserRestrictionSerializer(restrictions, many=True).data,
            status=status.HTTP_200_OK,
        )
