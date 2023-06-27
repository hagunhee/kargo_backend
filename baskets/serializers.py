from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Basket, Like, BasketItem
from users.models import User
from products.serializers import ProductPostSerializer


class LikeSerializer(ModelSerializer):
    product_post = ProductPostSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Like
        fields = (
            "pk",
            "user",
            "product_post",
        )


class BasketItemSerializer(ModelSerializer):
    product_post = ProductPostSerializer(
        read_only=True,
    )

    class Meta:
        model = BasketItem
        fields = (
            "pk",
            "basket",
            "product_post",
            "quantity",
        )


class BasketSerializer(ModelSerializer):
    basket_items = BasketItemSerializer(read_only=True, many=True)

    class Meta:
        model = Basket
        fields = ["user", "basket_items"]
