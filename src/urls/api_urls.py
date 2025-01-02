from django.urls import include, path
from restrictions import urls as restrictions_urls

urlpatterns = [
    path(
        "restrictions",
        include(
            restrictions_urls,
            namespace="restrictions",
        ),
    ),
]
