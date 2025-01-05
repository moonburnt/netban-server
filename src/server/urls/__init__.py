from django.conf import settings
from django.urls import include, path
from . import api_urls, schema_urls

urlpatterns = [
    path("api/v1/", include(api_urls.urlpatterns)),
]
if not settings.HEADLESS_MODE:
    from . import admin_urls

    urlpatterns.append(
        # TODO: make admin url's path configurable via envars, for security purposes
        path("admin/", include(admin_urls.urlpatterns)),
    )

# Only enable swagger view for debug mode
if settings.DEBUG:
    urlpatterns.append(
        path("api/schema/", include(schema_urls.urlpatters)),
    )
