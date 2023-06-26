from django.contrib import admin
from .models import Cart, CartItem, Like, PreOrder, PreOrderItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
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


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "cart",
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
