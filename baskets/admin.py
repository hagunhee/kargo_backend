from django.contrib import admin
from .models import Basket, BasketItem, Like, PreOrder, PreOrderItem


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
    )


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "basket",
        "product_post",
        "quantity",
    )


@admin.register(PreOrder)
class PreOrderAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
    )


@admin.register(PreOrderItem)
class PreOrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "pre_order",
        "product_post",
        "quantity",
    )
