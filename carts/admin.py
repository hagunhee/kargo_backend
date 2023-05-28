from django.contrib import admin
from .models import Cart, Like, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "product_post",
        "quantity",
    )
