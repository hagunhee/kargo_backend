from django.contrib import admin
from .models import Category, ExchangeRate


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "parent_category",
    )
    list_filter = ("parent_category",)
    search_fields = ("name",)


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "country",
        "exchange_rate",
    )
    list_filter = ("country",)
    search_fields = ("country",)
