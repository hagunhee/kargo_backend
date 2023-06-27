from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "message",
        "created_at",
        "updated_at",
    )
    list_filter = ("user",)
    search_fields = (
        "user",
        "message",
    )
