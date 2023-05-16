from django.db import models
from common.models import CommonModel


class Seller(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="sellers",
    )
    ##shop name은 유니크하여 중복을 방지한다.
    shop_name = models.CharField(max_length=100, unique=True)
    profile_imageURL = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.shop_name
