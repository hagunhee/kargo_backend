from django.db import models
from common.models import CommonModel


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
    name = models.CharField(max_length=255)
    original_price = models.PositiveIntegerField()
    stock_quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    imageURL = models.ImageField(upload_to="product_images", blank=True)
    is_deleted = models.BooleanField(default=False)
    weight = models.PositiveIntegerField(default=0)
    ##레퍼럴에 대한 커미션을 설정한다.
    commission = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class ProductPost(CommonModel):
    name = models.CharField(max_length=255, default="")
    # product와 연결하는데 manytomany로 연결한다.
    product = models.ManyToManyField(
        "products.Product",
        related_name="product_posts",
    )
    weight = models.ForeignKey(
        "products.Weight",
        on_delete=models.SET_NULL,
        related_name="product_posts",
        null=True,
        blank=True,
    )

    price_for_1 = models.PositiveIntegerField(null=True, blank=True)
    price_for_2 = models.PositiveIntegerField(null=True, blank=True)
    price_for_10 = models.PositiveIntegerField(null=True, blank=True)
    price_for_50 = models.PositiveIntegerField(null=True, blank=True)
    visibility = models.BooleanField(default=False)
    publish_time = models.DateTimeField()
    onsale = models.BooleanField(default=False)
    event_start_date = models.DateTimeField(blank=True, null=True)
    event_end_date = models.DateTimeField(blank=True, null=True)
    event_discount = models.PositiveIntegerField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name
