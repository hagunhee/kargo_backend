from django.db import models
from common.models import CommonModel


class Review(CommonModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveIntegerField()
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} / {self.rating}☆"
