from django.conf import settings
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import views, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any, Callable
from .serializers import (
    UserRestrictionSerializer,
    UserRestrictionRestrictSerializer,
)
from .services import UserRestrictionService


# TODO: maybe move this to core application
class FormattedResponseMixin:
    def finalize_response(
        self,
        request: Request,
        response: Response,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        ret = super().finalize_response(request, response, *args, **kwargs)
        ret_data = {
            "api_version": settings.API_VERSION,
        }

        if 199 < ret.status_code < 300:
            ret_data["error"] = False
        else:
            ret_data["error"] = True

        ret_data["data"] = ret.data
        ret.data = ret_data

        return ret


class UserRestrictionListView(FormattedResponseMixin, views.APIView):
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
            # TODO: patch the response serializer to add api response formatted data
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


class UserRestrictionRestrictView(FormattedResponseMixin, views.APIView):
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

        service = UserRestrictionService(
            user=serializer.validated_data["user"],
            group=serializer.validated_data.get("group", None),
        )
        try:
            restriction = service.restrict(
                restriction_type=serializer.validated_data["restriction_type"],
                restricted_by=serializer.validated_data["restricted_by"],
                reason=serializer.validated_data["restriction_reason"],
                length=serializer.validated_data.get(
                    "restriction_length", None
                ),
            )
        except Exception as e:
            return Response(
                data={
                    "code": str(getattr(e, "code", None) or type(e).__name__),
                    "detail": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                data=UserRestrictionSerializer(restriction).data,
                status=status.HTTP_200_OK,
            )
