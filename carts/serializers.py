from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Cart, Like, CartItem
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


class CartItemSerializer(ModelSerializer):
    product_post = ProductPostSerializer(
        read_only=True,
    )

    class Meta:
        model = CartItem
        fields = (
            "pk",
            "cart",
            "product_post",
            "quantity",
        )


class CartSerializer(ModelSerializer):
    cart_items = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = ["user", "cart_items"]
