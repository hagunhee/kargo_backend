from django.db import models
from common.models import CommonModel


class Product(CommonModel):
    brand = models.ForeignKey(
        "brands.Brand",
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
    name = models.CharField(max_length=255)
    original_price = models.PositiveIntegerField()
    stock_quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    imageURL = models.ImageField(upload_to="product_images", blank=True)
    is_deleted = models.BooleanField(default=False)
    ##레퍼럴에 대한 커미션을 설정한다.
    commission = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class ProductPost(CommonModel):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="product_posts",
    )
    price_for_1 = models.PositiveIntegerField()
    price_for_2 = models.PositiveIntegerField()
    price_for_10 = models.PositiveIntegerField()
    price_for_50 = models.PositiveIntegerField()
    visibility = models.BooleanField(default=False)
    publish_time = models.DateTimeField()
    onsale = models.BooleanField(default=False)
    event_start_date = models.DateTimeField(blank=True, null=True)
    event_end_date = models.DateTimeField(blank=True, null=True)
    event_discount = models.PositiveIntegerField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name
