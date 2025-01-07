from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any


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
