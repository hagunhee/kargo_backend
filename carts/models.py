from django.db import models
from common.models import CommonModel
from users.models import User


class Cart(CommonModel):
    # fk로 설정하고 unique로 설정하면 한 유저당 하나의 카트만 가질 수 있다.
    # product_post에 연결되어 있는 product의 weight를 더해서 총 무게를 계산한다.

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    total_weight = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)
    total_quantity = models.PositiveIntegerField(default=0)
    total_discount = models.PositiveIntegerField(default=0)
    total_price_after_discount = models.PositiveIntegerField(default=0)
    total_price_after_discount_and_shipping = models.PositiveIntegerField(default=0)
    total_shipping_fee = models.PositiveIntegerField(default=0)
    total_shipping_discount = models.PositiveIntegerField(default=0)
    total_shipping_fee_after_discount = models.PositiveIntegerField(default=0)
    total_shipping_fee_after_discount_and_coupon = models.PositiveIntegerField(default=0)
    total_shipping_fee_after_discount_and_coupon_and_point = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s cart"


class CartItem(CommonModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product_post = models.ForeignKey(
        "products.ProductPost", on_delete=models.CASCADE, related_name="items"
    )
    quantity = models.PositiveIntegerField()
    coupon = models.ForeignKey(
        "coupons.Coupon", on_delete=models.CASCADE, related_name="items", null=True, blank=True
    )

    def __str__(self):
        return f"Product {self.product_post.name} in {self.cart}"


class Like(CommonModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product_post = models.ManyToManyField("products.ProductPost", related_name="likes")

    def __str__(self):
        return f"{self.user.username} likes {self.product_post.name}"
