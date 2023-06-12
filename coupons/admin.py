from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "name",
        "role",
        "code",
        "discount_amount",
        "is_used",
        "used_at",
        "expired_at",
    ]

    # 생성된 코드 보기
    def view_code(self, obj):
        if obj.code_generated:
            return obj.code
        else:
            return "Code not generated yet"

    view_code.short_description = "Coupon Code"

    @admin.action(description="Generate codes for selected coupons")
    def generate_codes(self, request, queryset):
        for coupon in queryset:
            coupon.generate_code()
            coupon.save()

    actions = [
        generate_codes,
    ]
