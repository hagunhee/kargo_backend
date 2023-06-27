import strawberry
from strawberry import auto
from . import models
from products.types import ProductPostType
import typing
from users.types import UserType


@strawberry.django.type(models.Basket)
class BasketType:
    user: "UserType"
    basket_items: typing.List["BasketItemType"]
    shipments: auto
    total_weight: auto
    influencer_code: auto
    total_shipping_fee: auto
    total_coupon_discount: auto
    total_mileage_discount: auto
    total_original_price: auto
    total_discount_price: auto
    settle_price: auto
    free_shipping_FI: auto


@strawberry.django.type(models.BasketItem)
class BasketItemType:
    basket: auto
    product_post: "ProductPostType"
    quantity: auto
    coupon: auto
    influencer: auto
