from typing import Any

from django.contrib import admin

from .models import UserRestriction


@admin.register(UserRestriction)
class UserRestrictionAdmin(admin.ModelAdmin):
    list_display = [
        "platform_user",
        "restriction_type",
        # TODO: more fields, search by fields
    ]
