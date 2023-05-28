from django.db import models
from common.models import CommonModel

# user, code, discount_amount, is_used, used_at, expired_at,
# expired_at은 만료일이다. 만료일이 지나면 is_used를 True로 바꾼다.


class Coupon(CommonModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="coupons")
    brand = models.ForeignKey("users.Brand", on_delete=models.CASCADE, related_name="coupons")
    product_post = models.ForeignKey(
        "products.ProductPost", on_delete=models.CASCADE, related_name="coupons"
    )
    code = models.CharField(max_length=100, unique=True)
    discount_amount = models.PositiveIntegerField(default=0)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code
