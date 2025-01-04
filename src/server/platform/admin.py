from typing import Any

from django.contrib import admin

from .models import PlatformUser, PlatformGroup


@admin.register(PlatformUser)
class PlatformUserAdmin(admin.ModelAdmin):
    list_display = [
        "identifier",
    ]


@admin.register(PlatformGroup)
class PlatformGroupAdmin(admin.ModelAdmin):
    list_display = [
        "identifier",
    ]
