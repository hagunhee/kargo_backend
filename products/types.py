import strawberry
import typing
from . import models
from  medias.types import PhotoType, VideoType


@strawberry.django.type(models.Product)
class ProductType:
    id: int
    name: str
    brand: str
    category: str
    purchase_price: int
    original_price: int
    stock_quantity: int
    sales_quantity: int
    sale_price: int
    description: str
    imageurl: str
    is_deleted: bool
    weight: int
    commission: int


@strawberry.django.type(models.ProductPost)
class ProductPostType:
    id: int
    name: str
    products: typing.List[ProductType]
    price_for_1: int
    price_for_2: int
    price_for_10: int
    price_for_50: int
    visibility: bool
    publish_time: str
    onsale: bool
    event_type: str
    event_start_date: str
    event_end_date: str
    event_discount: int
    is_deleted: bool
    hit: int
    basket_cnt: int
    order_cnt: int
    seo_data: str
    grouppurchase_cnt: int
    photos: typing.List[PhotoType]
    video: "VideoType"

@strawberry.django.type(models.Category)
class Category:
    id: int
    name: str
    parent_category: str
