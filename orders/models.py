from django.db import models
from common.models import CommonModel


class OrderItem(CommonModel):
    class Status(models.IntegerChoices):
        PAID = 1, "Paid"
        READY = 2, "Ready"
        SHIPPED = 3, "Shipped"
        DELIVERED = 4, "Delivered"
        PAYMENT_COMPLETE = 5, "Payment Complete"
        CANCEL_REQUESTED = 6, "Cancel Requested"
        EXCHANGE_REQUESTED = 7, "Exchange Requested"
        RETURNING = 8, "Returning"
        EXCHANGED = 9, "Exchanged"
        REFUND_REQUESTED = 10, "Refund Requested"
        REFUNDED = 11, "Refunded"

    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="order_items")
    pre_order_item = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="order_items"
    )
    scmNo = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PAID)

    is_deleted = models.BooleanField(default=False)

    # status가 6,7,8,9,10,11일때는 claim 내용을 담을 수 있는
    # OrderClaimHandle을 생성해야함
    # 이 때 user와 order는 orderItem의 user와 order를 그대로 가져와야함
    def create_claim(self):
        pass

    def __str__(self):
        return f"{self.order.user.username} orders {self.product.name}"


class Order(CommonModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="orders")
    pre_order = models.ForeignKey(
        "carts.PreOrder",
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
        unique=True,
    )
    is_deleted = models.BooleanField(default=False)

    # 오더 아이템이 한건일때는 그냥 아이템의 상태를 가져오고
    # 오더 아이템이 여러건일때는 주문 x건이라는 식으로 표현해야함

    def __str__(self):
        if self.order_items.count() == 1:
            return f"{self.order_items.status}"
        else:
            return f"{self.order_items.count()} orders"


class OrderClaimHandle(CommonModel):
    # 여러 오더 아이템에 대한 클레임을
    # 한번에 처리할 수 있어야함
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="order_claim_handles"
    )
    order = models.ForeignKey(
        "orders.Order", on_delete=models.CASCADE, related_name="order_claim_handles"
    )

    claim_reason = models.CharField(max_length=100, blank=True, null=True)
    claim_detail = models.TextField(blank=True, null=True)
    claim_answer = models.TextField(blank=True, null=True)
    claim_answer_manager = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="order_claim_handles_answered",
        null=True,
        blank=True,
    )
    claim_answer_date = models.DateTimeField(blank=True, null=True)

    claim_account_name = models.CharField(max_length=100, blank=True, null=True)
    claim_account_bank = models.CharField(max_length=100, blank=True, null=True)
    claim_account_bank_code = models.CharField(max_length=100, blank=True, null=True)
    claim_date = models.DateTimeField()
    claim_handle = models.ForeignKey(
        "orders.OrderClaimHandle",
        on_delete=models.SET_NULL,
        related_name="order_items",
        null=True,
        blank=True,
    )
    # 반품건에 대한 송장번호
    return_scmNo = models.CharField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    # 총 구매액의 일정 포인트를 마일리지로 지급하는 메서드
    def give_mileage(self):
        pass

    def __str__(self):
        return f"{self.user.username} orders {self.product.name}"


class GroupPurchase(CommonModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="group_purchases")
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="group_purchases_by"
    )
    required_participants = (
        models.PositiveIntegerField()
    )  # 그룹퍼체이스 id를 검색하여 그룹퍼체이스에 참여한 유저들을 확인할 수 있다.
    end_time = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} group_purchases {self.product.name}"
