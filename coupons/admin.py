from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "brand",
        "code",
        "discount_amount",
        "is_used",
        "used_at",
        "expired_at",
    )

    list_filter = ("user", "brand")
    search_fields = (
        "user",
        "brand",
        "code",
    )
