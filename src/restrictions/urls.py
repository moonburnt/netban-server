from django.urls import include, path
from .views import UserRestrictionListView, UserRestrictionRestrictView

app_name = "restrictions"

urlpatterns = [
    path("", UserRestrictionListView.as_view()),
    path("/restrict", UserRestrictionRestrictView.as_view()),
]
