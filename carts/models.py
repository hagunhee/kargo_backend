from django.db import models
from common.models import CommonModel
from users.models import User
from orders.models import Order, OrderItem


class Cart(CommonModel):
    # fk로 설정하고 unique로 설정하면 한 유저당 하나의 카트만 가질 수 있다.
    # product_post에 연결되어 있는 product의 weight를 더해서 총 무게를 계산한다.

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    cart_items = models.ManyToManyField("carts.CartItem", related_name="carts")
    shipment = models.ForeignKey(
        "shipments.Shipment", on_delete=models.CASCADE, related_name="carts", null=True, blank=True
    )
    total_weight = models.PositiveIntegerField(default=0, blank=True, null=True)
    influencer_code = models.CharField(max_length=100, blank=True, null=True)
    total_shipping_fee = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_coupon_discount = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_mileage_discount = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_original_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_discount_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    settle_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    free_shipping_FI = models.BooleanField(default=False, blank=True, null=True)

    # 카트에서 결제하기 버튼을 누르면 pre_order를 생성한다.
    # pre_order는 order와 1:1 관계이다.
    # pre_order_item은 cart_item의 정보를 그대로 가져온다.
    # pre_order_item.total_mileage_discount = pre_order_item.product_post.mileage * pre_order_item.quantity
    # pre_order는 order_item과 1:N 관계이다.

    def __str__(self):
        return f"{self.user.username}'s cart"


class CartItem(CommonModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items_in_cart")
    product_post = models.ForeignKey(
        "products.ProductPost", on_delete=models.CASCADE, related_name="items"
    )
    quantity = models.PositiveIntegerField()
    coupon = models.ForeignKey(
        "coupons.Coupon", on_delete=models.CASCADE, related_name="items", null=True, blank=True
    )

    def __str__(self):
        return f"Product {self.product_post.name} in {self.cart}"


class PreOrderItem(CommonModel):
    pre_order = models.ForeignKey("carts.PreOrder", on_delete=models.CASCADE, related_name="items")
    product_post = models.ForeignKey(
        "products.ProductPost", on_delete=models.CASCADE, related_name="pre_order_items"
    )
    quantity = models.PositiveIntegerField()
    coupon = models.ForeignKey(
        "coupons.Coupon",
        on_delete=models.CASCADE,
        related_name="pre_order_items",
        null=True,
        blank=True,
    )
    total_coupon_discount = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_original_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_discount_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_mileage_discount = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_weight = models.PositiveIntegerField(default=0, blank=True, null=True)
    settle_price = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"Product {self.product_post.name} in {self.pre_order}"


class PreOrder(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pre_orders")
    shipment = models.ForeignKey(
        "shipments.Shipment",
        on_delete=models.CASCADE,
        related_name="pre_orders",
        null=True,
        blank=True,
    )
    total_coupon_discount = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_original_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_discount_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_mileage_discount = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_weight = models.PositiveIntegerField(default=0, blank=True, null=True)
    influencer_code = models.ForeignKey(
        "users.Influencer",
        on_delete=models.CASCADE,
        related_name="pre_orders",
        null=True,
        blank=True,
    )
    total_code_discount = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_shipping_fee = models.PositiveIntegerField(default=0, blank=True, null=True)
    free_shipping_fi = models.BooleanField(default=False, blank=True, null=True)
    settle_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    user_memo = models.TextField(blank=True, null=True)
    pg_name = models.CharField(max_length=100, blank=True, null=True)
    pg_result_code = models.CharField(max_length=100, blank=True, null=True)
    pg_tid = models.CharField(max_length=100, blank=True, null=True)
    pg_app_no = models.CharField(max_length=100, blank=True, null=True)
    pg_app_dt = models.DateTimeField(blank=True, null=True)
    pg_fail_reason = models.TextField(blank=True, null=True)
    pg_cancel_fi = models.BooleanField(default=False)
    pg_real_tax_supply_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    pg_real_tax_vat_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    pg_real_tax_free_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    is_deleted = models.BooleanField(default=False)
    is_taxfree = models.BooleanField(default=True)

    # 프리오더에서 결제가 완료되면 order테이블에 데이터를 입력해준다.
    # 프리오더에서 결제가 취소되면 카트로 데이터를 넘겨주며, 프리오더는 삭제된다.
    # 프리오더에서 결제가 취소되면 쿠폰을 다시 사용가능하게 만들어준다.
    # 프리오더에서 결제가 완료되면 쿠폰을 사용불가능하게 만들어준다.
    # 프리오더에서 결제가 완료되면 마일리지를 사용한 만큼 차감해준다.
    # 프리오더에서 결제가 취소되면 마일리지를 다시 돌려준다.
    # 프리오더에서 결제가 완료되면 상품의 재고를 차감해준다.
    # 프리오더에서 결제가 취소되면 상품의 재고를 다시 돌려준다.
    # 프리오더에서 결제가 완료되면 상품의 판매량을 증가시켜준다.
    # 프리오더에서 결제가 취소되면 상품의 판매량을 다시 돌려준다.
    def save(self, *args, **kwargs):
        if self.pg_cancel_fi:
            self.cart = Cart.objects.get(user=self.user)
            self.cart_items = CartItem.objects.filter(cart=self.cart)
            for cart_item in self.cart_items:
                cart_item.product_post.stock += cart_item.quantity
                cart_item.product_post.save()
                cart_item.product_post.sales_volume -= cart_item.quantity
                cart_item.product_post.save()
        else:
            self.order = Order.objects.create(
                user=self.user,
                total_weight=self.total_weight,
                total_shipping_fee=self.total_shipping_fee,
                total_coupon_discount=self.total_coupon_discount,
                total_mileage_discount=self.total_mileage_discount,
                total_discount_price=self.total_discount_price,
                total_original_price=self.total_original_price,
                total_price=self.total_price,
                free_shipping_fi=self.free_shipping_fi,
                influencer_code=self.influencer_code,
                exchange_rate=self.exchange_rate,
                user_memo=self.user_memo,
                pg_name=self.pg_name,
                pg_result_code=self.pg_result_code,
                pg_tid=self.pg_tid,
                pg_app_no=self.pg_app_no,
                pg_app_dt=self.pg_app_dt,
                pg_fail_reason=self.pg_fail_reason,
                pg_cancel_fi=self.pg_cancel_fi,
                pg_real_tax_supply_price=self.pg_real_tax_supply_price,
                pg_real_tax_vat_price=self.pg_real_tax_vat_price,
                pg_real_tax_free_price=self.pg_real_tax_free_price,
            )
            self.order_items = OrderItem.objects.filter(order=self.order)
            for order_item in self.order_items:
                order_item.product_post.stock -= order_item.quantity
                order_item.product_post.save()
                order_item.product_post.sales_volume += order_item.quantity
                order_item.product_post.save()
                if order_item.coupon:
                    order_item.coupon.is_used = True
                    order_item.coupon.save()
                if order_item.product_post.mileage:
                    self.user.mileage -= order_item.product_post.mileage
                    self.user.save()
            self.cart = Cart.objects.get(user=self.user)
            self.cart_items = CartItem.objects.filter(cart=self.cart)
            self.cart_items.delete()
            self.cart.delete()

    def __str__(self):
        return f"{self.user.username}'s pre-order"


class Like(CommonModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product_post = models.ManyToManyField("products.ProductPost", related_name="likes")

    def __str__(self):
        return f"{self.user.username} likes {self.product_post.name}"
