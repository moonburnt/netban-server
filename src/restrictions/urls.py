from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import UserRestrictionView

app_name = "restrictions"

# router = SimpleRouter()
# router.register("", UserRestrictionView, basename="user_restrictions")

urlpatterns = [
    # path("", include(router.urls)),
    path("", UserRestrictionView.as_view())
]
