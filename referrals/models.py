from django.db import models
from common.models import CommonModel


class Referral(CommonModel):
    ##셀러아이디와 프로덕트아이디를 FK로 받아온다.
    seller = models.ForeignKey(
        "sellers.Seller",
        on_delete=models.CASCADE,
        related_name="referrals",
    )
    product = models.ForeignKey(
        "products.Product",
        related_name="referrals",
        on_delete=models.SET_NULL,
        null=True,
    )
    ##리퍼럴코드는 유니크하여 중복을 방지한다.
    referral_code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.referral_code
