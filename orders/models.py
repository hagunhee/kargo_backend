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
    pre_order_item = models.OneToOneField(
        "baskets.PreOrderItem", on_delete=models.SET_NULL, related_name="order_item", null=True
    )
    scmNo = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PAID)
    refund_amount = models.PositiveIntegerField(default=0)

    is_deleted = models.BooleanField(default=False)

    # status가 6,7,8,9,10,11일때는 claim 내용을 담을 수 있는
    # OrderClaimHandle을 생성해야함
    # 이 때 user와 order는 orderItem의 user와 order를 그대로 가져와야함
    def create_claim(self):
        pass

    def __str__(self):
        return f"{self.order.user.username} orders {self.pre_order_item.name}"


class Order(CommonModel):
    class Status(models.IntegerChoices):
        PAID = 1, "Paid"
        READY = 2, "Ready"
        SHIPPED = 3, "Shipped"
        DELIVERED = 4, "Delivered"
        PAYMENT_COMPLETE = 5, "Payment Complete"
        # 1,2,3,4,5의 플로우에서 벗어날경우 상세보기에서 표현해야함
        ORDER_DETAIL = 6, "Order Detail"

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="orders")
    pre_order = models.OneToOneField(
        "baskets.PreOrder", on_delete=models.SET_NULL, related_name="order", null=True
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

    order_items = models.ManyToManyField(
        "orders.OrderItem", related_name="order_claim_handles", blank=True
    )
    # 클레임 발생과 동시에 금액을 넘겨받아야 한다.
    # 클레임이 완료되면 오더에 금액을 넘겨줘야 한다.
    claim_amount = models.PositiveIntegerField()
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

    # 반품건에 대한 송장번호
    return_scmNo = models.CharField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    # 총 구매액의 일정 포인트를 마일리지로 지급하는 메서드
    def give_mileage(self):
        pass


class GroupPurchase(CommonModel):
    users = models.ManyToManyField(
        "users.User", related_name="group_purchases", through="GroupPurchaseUser"
    )

    product_post = models.ForeignKey(
        "products.ProductPost",
        on_delete=models.CASCADE,
        related_name="group_purchases",
        default=None,
    )
    required_participants = models.PositiveIntegerField()
    end_time = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_user.username} group_purchases {self.product_post.product.name}"

    @property
    def first_user(self):
        return self.users.order_by("grouppurchaseuser__created_at").first()

    @property
    def is_participant_goal_reached(self):
        return self.users.count() >= self.required_participants

    def close_group_purchase(self):
        """
        참여한 사용자의 수와 필요한 참여자의 수를 비교하여
        필요한 참여자의 수에 도달하면 그룹 구매를 마감합니다.
        """
        if self.users.count() >= self.required_participants:
            self.is_closed = True
            self.save()

    def save(self, *args, **kwargs):
        """
        객체가 저장될 때마다 close_group_purchase 메서드를 호출하여
        필요한 참여자 수에 도달했는지 확인하고, 도달했다면 그룹 구매를 마감합니다.
        """
        self.close_group_purchase()
        super().save(*args, **kwargs)


class GroupPurchaseUser(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    group_purchase = models.ForeignKey("orders.GroupPurchase", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "group_purchase")
