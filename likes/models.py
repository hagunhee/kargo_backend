from django.db import models
from common.models import CommonModel


class Like(CommonModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="likes")
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="liked_by"
    )
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ["user", "product"]

    def __str__(self):
        return f"{self.user.username} likes {self.product.name}"
