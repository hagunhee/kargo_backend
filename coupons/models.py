from django.db import models
from common.models import CommonModel
from utils import HashidHandler

# user, code, discount_amount, is_used, used_at, expired_at,
# expired_at은 만료일이다. 만료일이 지나면 is_used를 True로 바꾼다.


class Coupon(CommonModel):
    class CouponTypeChoices(models.TextChoices):
        ALL = ("all", "All Items")
        BRAND = ("brand", "Specific Brands")
        PRODUCT = ("product", "Specific ProductPosts")

    name = models.CharField(max_length=255, default="", null=True, blank=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="coupons")
    role = models.CharField(
        choices=CouponTypeChoices.choices, max_length=50, default=CouponTypeChoices.ALL
    )
    brands = models.ManyToManyField("users.Brand", blank=True)
    product_posts = models.ManyToManyField("products.ProductPost", blank=True)
    code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    discount_amount = models.PositiveIntegerField(default=0)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)

    def generate_code(self):
        if not self.code:
            hashid_handler = HashidHandler()
            self.code = hashid_handler.encode_hash(self.pk)
            self.save()
