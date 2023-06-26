from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "file",
        "description",
        "product_post",
        "brand",
        "influencer_posting",
        "reviews",
        "influencer",
        "orderclaimhandle",
        "notification",
        "notice",
        "userQnA",
    )
    list_filter = (
        "product_post",
        "brand",
        "influencer_posting",
        "reviews",
        "influencer",
        "orderclaimhandle",
        "notification",
        "notice",
        "userQnA",
    )
    search_fields = (
        "product_post",
        "brand",
        "influencer_posting",
        "reviews",
        "influencer",
        "orderclaimhandle",
        "notification",
        "notice",
        "userQnA",
    )


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "file",
        "description",
        "product_post",
        "influencer_posting",
    )
    list_filter = (
        "product_post",
        "influencer_posting",
    )
    search_fields = (
        "product_post",
        "influencer_posting",
    )
