from django.db import models
from common.models import CommonModel

##패런츠 카테고리 필드를 FK로 설정하여 동일한 테이블내의 다른 카테고리를 부모로 갖을 수 있다.


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    imageURL = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class ExchangeRate(CommonModel):
    # 국가별 환율을 저장하는 테이블 bigdecimalfield를 사용한다.
    country = models.CharField(max_length=255)
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=10)
