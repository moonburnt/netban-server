from typing import Any

from django.contrib import admin

from .models import PlatformUser


@admin.register(PlatformUser)
class PlatformUserAdmin(admin.ModelAdmin):
    list_display = [
        "user_id",
    ]
