from django.db import models
from common.models import CommonModel

##user, product 필드를 FK로 설정하여 유저와 프로덕트를 연결한다.
##quantity, order_price, refferral_id, is_deleted 필드를 추가한다.


class Order(CommonModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    order_price = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)

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
