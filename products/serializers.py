from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Product, ProductPost


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "brand",
            "category",
            "name",
            "original_price",
            "stock_quantity",
            "description",
            "imageURL",
            "is_deleted",
            "commission",
        )


class ProductPostSerializer(ModelSerializer):
    class Meta:
        model = ProductPost
        fields = (
            "pk",
            "product",
            "name",
            "price_for_1",
            "price_for_2",
            "price_for_10",
            "price_for_50",
            "visibility",
            "publish_time",
            "onsale",
            "event_start_date",
            "event_end_date",
            "event_discount",
            "is_deleted",
        )
