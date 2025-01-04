from django.urls import include, path
from server.restrictions import urls as restrictions_urls

urlpatterns = [
    path(
        "restrictions",
        include(
            (restrictions_urls.urlpatterns, "restrictions"),
            namespace="restrictions",
        ),
    ),
]
