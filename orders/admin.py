from django.contrib import admin
from .models import Order, GroupPurchase


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_deleted",
    )

    list_filter = ("user",)
    search_fields = ("user",)


@admin.register(GroupPurchase)
class GroupPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "display_users",
        "product_post",
        "required_participants",
        "end_time",
        "is_closed",
        "is_deleted",
    )

    def display_users(self, obj):
        return obj.users.count()

    display_users.short_description = "Users Count"

    list_filter = (
        "users",
        "product_post",
    )
    search_fields = (
        "users",
        "product_post",
    )
