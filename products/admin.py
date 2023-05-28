from django.contrib import admin
from .models import Product, ProductPost


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "brand",
        "category",
        "name",
        "original_price",
        "stock_quantity",
        "description",
        "imageURL",
        "is_deleted",
        "commission",
    )

    list_filter = ("brand", "category", "is_deleted")
    search_fields = ("name",)


@admin.register(ProductPost)
class ProductPostAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "name",
        "price_for_1",
        "price_for_2",
        "price_for_10",
        "price_for_50",
        "visibility",
        "publish_time",
        "onsale",
        "event_start_date",
        "event_end_date",
        "event_discount",
        "is_deleted",
    )

    list_filter = ("product", "visibility", "onsale", "is_deleted")
    search_fields = ("product",)
