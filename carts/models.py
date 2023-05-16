from django.db import models
from common.models import CommonModel


class Cart(CommonModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="carts")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="carts")
    quantity = models.PositiveIntegerField()
    referral_id = models.CharField(max_length=100, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} carts {self.product.name}"
