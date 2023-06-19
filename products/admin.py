from django.contrib import admin
from .models import Product, ProductPost, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "category",
        "original_price",
        "stock_quantity",
        "description",
        "is_deleted",
        "weight",
        "commission",
        "created_at",
        "updated_at",
    )

    list_filter = ("brand", "category", "is_deleted")
    search_fields = ("name",)


@admin.register(ProductPost)
class ProductPostAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_product",
        "display_weights",
        "total_weight",
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

    list_filter = ("visibility", "onsale", "is_deleted")
    search_fields = ("name",)

    def display_product(self, obj):
        return ", ".join([product.name for product in obj.product.all()])

    display_product.short_description = "Products"

    def display_weights(self, obj):
        return ", ".join([str(product.weight) for product in obj.product.all()])

    display_weights.short_description = "Weights of Each Product"

    def total_weight(self, obj):
        return sum([product.weight for product in obj.product.all()])

    total_weight.short_description = "Total Weight"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parent_category",
    )
    list_filter = ("parent_category",)
    search_fields = ("name",)
