from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from typing import Any


class HasCorrectAPIVersionHeader(BasePermission):
    code = "unsupported_version"
    message = "Netban-Api-Version header mismatch"

    def has_permission(self, request: Request, view: Any) -> bool:
        return bool(
            request.META.get("HTTP_NETBAN_API_VERSION", None)
            == settings.API_VERSION
        )
