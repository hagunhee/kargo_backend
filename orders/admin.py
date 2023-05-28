from django.contrib import admin
from .models import Order, GroupPurchase


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "quantity",
        "order_price",
        "is_deleted",
    )

    list_filter = ("user", "product")
    search_fields = (
        "user",
        "product",
    )


@admin.register(GroupPurchase)
class GroupPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "required_participants",
        "end_time",
        "is_deleted",
    )

    list_filter = (
        "user",
        "product",
    )
    search_fields = (
        "user",
        "product",
    )
