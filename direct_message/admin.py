from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "sender",
        "receiver",
        "message",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "sender",
        "receiver",
    )
    search_fields = (
        "sender",
        "receiver",
    )
