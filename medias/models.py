from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    # cloudfront images 를 사용하여 이미지를 불러온다.

    file = models.URLField()
    description = models.CharField(max_length=255, blank=True, null=True)
    product_post = models.ForeignKey(
        "products.ProductPost",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    brand = models.ForeignKey(
        "users.Brand",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    influencer_posting = models.ForeignKey(
        "users.InfluencerPosting",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    reviews = models.ForeignKey(
        "reviews.Review",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    influencer = models.ForeignKey(
        "users.Influencer",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    orderclaimhandle = models.ForeignKey(
        "orderclaims.OrderClaimHandle",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    notification = models.ForeignKey(
        "notifications.Notification",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    notice = models.ForeignKey(
        "notifications.Notice",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    # photo = models.ImageField(upload_to="photos")
    # product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="photos")
    # is_deleted = models.BooleanField(default=False)
    # is_thumbnail = models.BooleanField(default=False)
    # order = models.PositiveIntegerField(default=0)
    # imgurl = models.URLField(null=True, blank=True)
    #
    # def __str__(self):
    #     return f"{self.product} / {self.order}"
    pass


class Video(CommonModel):
    file = models.URLField()
    description = models.CharField(max_length=255, blank=True, null=True)
    product_post = models.ForeignKey(
        "products.ProductPost",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="videos",
    )
    influencer_posting = models.ForeignKey(
        "users.InfluencerPosting",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="videos",
    )
