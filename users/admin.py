from django.contrib import admin
from .models import User, UserAddress, Influencer, Brand, InfluencerPosting


class UserAddressInline(admin.StackedInline):
    model = UserAddress  # UserAddress 모델을 대상으로 함
    extra = 0


class InfluencerInline(admin.StackedInline):
    model = Influencer
    extra = 0


class InfluencerPostingInline(admin.StackedInline):
    model = InfluencerPosting
    extra = 0


class BrandInline(admin.StackedInline):
    model = Brand
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "username", "email", "first_name", "last_name", "date_joined", "last_login", "role")  # 'id' 또는 'pk'를 추가

    fieldsets = (
        (
            "User Profile",
            {
                "fields": (
                    "role",
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "date_joined",
                    "last_login",
                    "following",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
                "classes": ("wide",),
            },
        ),
    )
    inlines = [
        UserAddressInline,
        InfluencerInline,
        BrandInline,
    ]  # UserAddressInline을 UserAdmin에 추가


@admin.register(Influencer)
class InfluencerAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Influencer Information",
            {
                "fields": (
                    "pk",
                    "shop_name",
                    "influencer_code",
                    "profile_imageURL",
                )
            },
        ),
    )
    inlines = [
        InfluencerPostingInline,
    ]
