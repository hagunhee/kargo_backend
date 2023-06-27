from django.db import models
from common.models import CommonModel
import typing

class Product(CommonModel):
    brand = models.ForeignKey(
        "users.Brand",
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
    )
    # 매입가격
    purchase_price = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)
    original_price = models.PositiveIntegerField()
    stock_quantity = models.PositiveIntegerField()
    sales_quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    sale_price = models.PositiveIntegerField()
    description = models.TextField(blank=True, default="")
    imageurl = models.ImageField(upload_to="product_images", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    weight = models.PositiveIntegerField(default=0)
    ##레퍼럴에 대한 커미션을 설정한다.
    commission = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name


class ProductPost(CommonModel):
    class EventType(models.TextChoices):
        NORMAL = "NORMAL", "normal"
        EVENT = "EVENT", "event"

    name = models.CharField(max_length=255, default="")
    # product와 연결하는데 manytomany로 연결한다.
    product = models.ManyToManyField(
        "products.Product",
        related_name="product_posts",
    )

    price_for_1 = models.PositiveIntegerField(null=True, blank=True)
    price_for_2 = models.PositiveIntegerField(null=True, blank=True)
    price_for_10 = models.PositiveIntegerField(null=True, blank=True)
    price_for_50 = models.PositiveIntegerField(null=True, blank=True)
    visibility = models.BooleanField(default=False, null=True, blank=True)
    publish_time = models.DateTimeField(null=True, blank=True)
    onsale = models.BooleanField(default=False, null=True, blank=True)
    event_type = models.CharField(
        default=EventType.NORMAL, choices=EventType.choices, max_length=30
    )
    event_start_date = models.DateTimeField(blank=True, null=True)
    event_end_date = models.DateTimeField(blank=True, null=True)
    event_discount = models.PositiveIntegerField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    hit = models.PositiveIntegerField(default=0, null=True, blank=True)
    basket_cnt = models.PositiveIntegerField(default=0, null=True, blank=True)
    order_cnt = models.PositiveIntegerField(default=0, null=True, blank=True)
    seo_data = models.TextField(blank=True, null=True)
    grouppurchase_cnt = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
