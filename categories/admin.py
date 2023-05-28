from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parent_category",
    )
    list_filter = ("parent_category",)
    search_fields = ("name",)
