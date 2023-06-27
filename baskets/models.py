from __future__ import annotations
from django.db import models
from common.models import CommonModel
from users.models import User
from orders.models import Order, OrderItem

from collections import OrderedDict
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Generator

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.http import HttpRequest
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


if TYPE_CHECKING:  # pragma: no cover
    from django.db.models.manager import RelatedManager

BASKET_ID_SESSION_KEY = "BASKET_ID"


class BasketManager(models.Manager["BaseBasket"]):
    def get_or_create_from_request(
        self,
        request: HttpRequest,
    ) -> tuple[BaseBasket, bool]:
        """
        Get basket from request or create a new one.
        If user is logged in session basket gets merged into a user basket.

        Returns:
            tuple: (basket, created)
        """
        if not hasattr(request, "session"):
            request.session = {}
        try:
            session_basket_id = request.session[BASKET_ID_SESSION_KEY]
            session_basket = self.get(id=session_basket_id, user=None)
        except (KeyError, self.model.DoesNotExist):
            session_basket = None

        if hasattr(request, "user") and request.user.is_authenticated:
            try:
                basket, created = self.get_or_create(user_pk=request.user.pk)
            except self.model.MultipleObjectsReturned:
                # User has multiple baskets, merge them.
                baskets = list(self.filter(user=request.user.pk))
                basket, created = baskets[0], False
                for other in baskets[1:]:
                    basket.merge(other)

            if session_basket:
                # Merge session basket into user basket.
                basket.merge(session_basket)

            if BASKET_ID_SESSION_KEY in request.session:
                # Delete session basket id from session so that it doesn't get
                # re-fetched while user is still logged in.
                del request.session[BASKET_ID_SESSION_KEY]
        else:
            basket, created = session_basket or self.create(), not session_basket
            request.session[BASKET_ID_SESSION_KEY] = basket.pk

        return basket, created


class Basket(CommonModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="baskets",
        null=True,
        blank=True,
    )
    basket_items = models.ManyToManyField("baskets.BasketItem", related_name="baskets")
    shipments = models.ForeignKey(
        "shipments.Shipment",
        on_delete=models.CASCADE,
        related_name="baskets",
        null=True,
        blank=True,
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

    # objects필드는 커스텀매니저를 설정하는 것이다.
    # 커스텀매니저는 모델의 메소드를 확장할 수 있게 해준다.
    objects = BasketManager()
    items: RelatedManager[BaseBasketItem]

    _cached_items: list[BaseBasketItem] | None = None

    class Meta:
        verbose_name = _("Basket")
        verbose_name_plural = _("Baskets")
        ordering = ["created_at"]

    def __str__(self) -> str:
        return str(self.pk) if self.pk else "(unsaved)"

    def __iter__(self) -> Generator[BaseBasketItem, None, None]:
        for item in self.items.all():
            yield item

    def update(self, request: HttpRequest) -> None:
        """
        Process basket with modifiers defined in ``SALESMAN_BASKET_MODIFIERS``.
        This method sets ``subtotal``, ``total`` and ``extra_rows`` attributes on the
        basket and updates the items. Should be called every time the basket item is
        added, removed or updated or basket extra is updated.

        Args:
            request (HttpRequest): Django request
        """
        from .modifiers import basket_modifiers_pool

        items = self.get_items()

        # Setup basket and items.
        for modifier in basket_modifiers_pool.get_modifiers():
            modifier.setup_basket(self, request)
            for item in items:
                modifier.setup_item(item, request)

        self.extra_rows: dict[str, Any] = OrderedDict()
        self.subtotal = Decimal(0)
        self.total = Decimal(0)

        # Process basket items.
        for item in items:
            item.update(request)
            self.subtotal += item.total
        self.total = self.subtotal

        # Finalize items and process basket.
        for modifier in basket_modifiers_pool.get_modifiers():
            for item in items:
                modifier.finalize_item(item, request)
            modifier.process_basket(self, request)

        # Finalize basket.
        for modifier in basket_modifiers_pool.get_modifiers():
            modifier.finalize_basket(self, request)

        self._cached_items = items

    def add(
        self,
        product: Product,
        quantity: int = 1,
        ref: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> BaseBasketItem:
        """
        Add product to the basket.

        Returns:
            BasketItem: BasketItem instance
        """
        BasketItem = get_salesman_model("BasketItem")
        if not ref:
            ref = BasketItem.get_product_ref(product)
        try:
            item = self.items.get(ref=ref)
            item.quantity += quantity
            item.extra = extra or item.extra
            item.save(update_fields=["quantity", "extra", "date_updated"])
        except BasketItem.DoesNotExist:
            item = BasketItem.objects.create(
                basket=self,
                product=product,
                quantity=quantity,
                ref=ref,
                extra=extra or {},
            )
        self._cached_items = None
        return item

    def remove(self, ref: str) -> None:
        """
        Remove item with given ``ref`` from the basket.

        Args:
            ref (str): Item ref to remove
        """
        item = self.find(ref)
        if item:
            item.delete()
            self._cached_items = None

    def find(self, ref: str) -> BaseBasketItem | None:
        """
        Find item with given ``ref`` in the basket.

        Args:
            ref (str): Item ref

        Returns:
            Optional[BaseBasketItem]: Basket item if found.
        """
        if self._cached_items is not None:
            try:
                return [item for item in self._cached_items if item.ref == ref][0]
            except IndexError:
                return None
        return self.items.filter(ref=ref).first()

    def clear(self) -> None:
        """
        Clear all items from the basket.
        """
        self.items.all().delete()
        self._cached_items = None

    @transaction.atomic
    def merge(self, other: BaseBasket) -> None:
        """
        Merge other basket with this one, delete afterwards.

        Args:
            other (Basket): Basket which to merge
        """
        for item in other:
            try:
                existing = self.items.get(ref=item.ref)
                existing.quantity += item.quantity
                existing.save(update_fields=["quantity"])
            except item.DoesNotExist:
                item.basket = self
                item.save(update_fields=["basket"])
        other.delete()
        self._cached_items = None

    def get_items(self) -> list[BaseBasketItem]:
        """
        Returns items from cache or stores new ones.
        """
        if self._cached_items is None:
            self._cached_items = list(self.items.all().prefetch_related("product"))
        return self._cached_items

    @property
    def count(self) -> int:
        """
        Returns basket item count.
        """
        if self._cached_items is not None:
            return len(self._cached_items)
        return self.items.count()

    @property
    def quantity(self) -> int:
        """
        Returns the total quantity of all items in a basket.
        """
        if self._cached_items is not None:
            return sum([item.quantity for item in self._cached_items])
        aggr = self.items.aggregate(quantity=models.Sum("quantity"))
        return aggr["quantity"] or 0


class BasketItem(CommonModel):
    # basket = models.ForeignKey(
    #     app_settings.SALESMAN_BASKET_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name="items",
    #     verbose_name=_("Basket"),
    # )
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="items_in_basket")
    product_post = models.ForeignKey(
        "products.ProductPost", on_delete=models.CASCADE, related_name="items"
    )
    quantity = models.PositiveIntegerField()
    coupon = models.ForeignKey(
        "coupons.Coupon", on_delete=models.CASCADE, related_name="items", null=True, blank=True
    )
    influencer = models.ForeignKey(
        "users.Influencer", on_delete=models.CASCADE, related_name="baskets", null=True, blank=True
    )

    def __str__(self):
        return f"Product {self.product_post.name} in {self.basket}"

    # Reference to this basket item, used to determine item duplicates.
    ref = models.SlugField(_("Reference"), max_length=128)

    # Generic relation to product.
    product_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField(_("Product id"))
    product = GenericForeignKey("product_content_type", "product_id")

    quantity = models.PositiveIntegerField(_("Quantity"), default=1)

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
        unique_together = ("basket", "ref")
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        # Set default ref.
        if not self.ref and self.product:
            self.ref = self.get_product_ref(self.product)
        super().save(*args, **kwargs)

    def update(self, request: HttpRequest) -> None:
        """
        Process items with modifiers defined in ``SALESMAN_BASKET_MODIFIERS``.
        This method sets ``unit_price``, ``subtotal``, ``total`` and ``extra_rows``
        attributes on the item. Should be called every time the basket item
        is added, removed or updated.

        Args:
            request (HttpRequest): Django request
        """
        from .modifiers import basket_modifiers_pool

        self.extra_rows: dict[str, Any] = OrderedDict()
        if self.product:
            self.unit_price = Decimal(self.product.get_price(request))
        else:
            self.unit_price = Decimal(0)
        self.subtotal = self.unit_price * self.quantity
        self.total = self.subtotal

        for modifier in basket_modifiers_pool.get_modifiers():
            modifier.process_item(self, request)

    @property
    def name(self) -> str:
        """
        Returns product `name`.
        """
        return str(self.product.name) if self.product else "(no name)"

    @property
    def code(self) -> str:
        """
        Returns product `name`.
        """
        return str(self.product.code) if self.product else "(no code)"

    @classmethod
    def get_product_ref(cls, product: Product) -> str:
        """
        Returns default item ``ref`` for given product.

        Args:
            product (Product): Product instance

        Returns:
            str: Item ref
        """
        return slugify(f"{product._meta.label}-{product.id}")


class PreOrderItem(CommonModel):
    pre_order = models.ForeignKey(
        "baskets.PreOrder", on_delete=models.CASCADE, related_name="items"
    )
    product_post = models.ForeignKey(
        "products.ProductPost", on_delete=models.CASCADE, related_name="pre_order_items"
    )
    influencer = models.ForeignKey(
        "users.Influencer",
        on_delete=models.CASCADE,
        related_name="pre_order_items",
        null=True,
        blank=True,
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
    shipments = models.ForeignKey(
        "shipments.Shipment",
        on_delete=models.CASCADE,
        related_name="pre_orders",
        null=True,
        blank=True,
    )
    total_coupon_discount = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_original_price = models.PositiveIntegerField(default=0, blank=True, null=True)
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
    free_shipping_fi = models.BooleanField(default=False, blank=True, null=True)
    total_shipping_fee = models.PositiveIntegerField(default=0, blank=True, null=True)
    total_discount_price = models.PositiveIntegerField(default=0, blank=True, null=True)
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

    # # 프리오더에서 결제가 완료되면 order테이블에 데이터를 입력해준다.
    # # 프리오더에서 결제가 취소되면 카트로 데이터를 넘겨주며, 프리오더는 삭제된다.
    # # 프리오더에서 결제가 취소되면 쿠폰을 다시 사용가능하게 만들어준다.
    # # 프리오더에서 결제가 완료되면 쿠폰을 사용불가능하게 만들어준다.
    # # 프리오더에서 결제가 완료되면 마일리지를 사용한 만큼 차감해준다.
    # # 프리오더에서 결제가 취소되면 마일리지를 다시 돌려준다.
    # # 프리오더에서 결제가 완료되면 상품의 재고를 차감해준다.
    # # 프리오더에서 결제가 취소되면 상품의 재고를 다시 돌려준다.
    # # 프리오더에서 결제가 완료되면 상품의 판매량을 증가시켜준다.
    # # 프리오더에서 결제가 취소되면 상품의 판매량을 다시 돌려준다.
    # def save(self, *args, **kwargs):
    #     if self.pg_cancel_fi:
    #         self.basket = Basket.objects.get(user=self.user)
    #         self.basket_items = BasketItem.objects.filter(basket=self.basket)
    #         for basket_item in self.basket_items:
    #             basket_item.product_post.stock += basket_item.quantity
    #             basket_item.product_post.save()
    #             basket_item.product_post.sales_volume -= basket_item.quantity
    #             basket_item.product_post.save()
    #     else:
    #         self.order = Order.objects.create(
    #             user=self.user,
    #             total_weight=self.total_weight,
    #             total_shipping_fee=self.total_shipping_fee,
    #             total_coupon_discount=self.total_coupon_discount,
    #             total_mileage_discount=self.total_mileage_discount,
    #             total_discount_price=self.total_discount_price,
    #             total_original_price=self.total_original_price,
    #             settle_price=self.settle_price,
    #             free_shipping_fi=self.free_shipping_fi,
    #             influencer_code=self.influencer_code,
    #             exchange_rate=self.exchange_rate,
    #             user_memo=self.user_memo,
    #             pg_name=self.pg_name,
    #             pg_result_code=self.pg_result_code,
    #             pg_tid=self.pg_tid,
    #             pg_app_no=self.pg_app_no,
    #             pg_app_dt=self.pg_app_dt,
    #             pg_fail_reason=self.pg_fail_reason,
    #             pg_cancel_fi=self.pg_cancel_fi,
    #             pg_real_tax_supply_price=self.pg_real_tax_supply_price,
    #             pg_real_tax_vat_price=self.pg_real_tax_vat_price,
    #             pg_real_tax_free_price=self.pg_real_tax_free_price,
    #         )
    #         self.order_items = OrderItem.objects.filter(order=self.order)
    #         for order_item in self.order_items:
    #             order_item.product_post.stock -= order_item.quantity
    #             order_item.product_post.save()
    #             order_item.product_post.sales_volume += order_item.quantity
    #             order_item.product_post.save()
    #             if order_item.coupon:
    #                 order_item.coupon.is_used = True
    #                 order_item.coupon.save()
    #             if order_item.product_post.mileage:
    #                 self.user.mileage -= order_item.product_post.mileage
    #                 self.user.save()
    #         self.basket = Basket.objects.get(user=self.user)
    #         self.basket_items = BasketItem.objects.filter(basket=self.basket)
    #         self.basket_items.delete()
    #         self.basket.delete()

    def __str__(self):
        return f"{self.user.username}'s pre-order"


class Like(CommonModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product_post = models.ManyToManyField("products.ProductPost", related_name="likes")

    def __str__(self):
        return f"{self.user.username} likes {self.product_post.name}"
