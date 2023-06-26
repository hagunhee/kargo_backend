# reviews 모델의 admin을 만든다
# admin.py
from django.contrib import admin
from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "product_post",
        "rating",
        "content",
        "imgurl",
        "is_deleted",
    )
    list_filter = (
        "user",
        "product_post",
        "rating",
        "content",
        "imgurl",
        "is_deleted",
    )
    search_fields = (
        "user",
        "product_post",
        "rating",
        "content",
        "imgurl",
        "is_deleted",
    )
