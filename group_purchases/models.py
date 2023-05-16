from django.db import models
from common.models import CommonModel


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
