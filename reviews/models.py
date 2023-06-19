from django.db import models
from common.models import CommonModel


class Review(CommonModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews")
    product_post = models.ForeignKey(
        "products.ProductPost",
        on_delete=models.CASCADE,
        related_name="reviews",
        default=None,
        null=True,
        blank=True,
    )
    rating = models.PositiveIntegerField()
    content = models.TextField()
    imgurl = models.URLField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} / {self.rating}☆"
