from django.conf import settings
from django.contrib import admin
from django.urls import include, path

admin.autodiscover()

urlpatterns = [
    # TODO: make admin url's path configurable via envars, for security purposes
    path("", admin.site.urls),
]
