from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User, UserAddress, Influencer, Brand


class UserAddressSerializer(ModelSerializer):
    class Meta:
        model = UserAddress
        fields = (
            "address",
            "address_detail",
            "zipcode",
            "phone_number",
            "is_default",
        )
        extra_kwargs = {
            "address": {"required": True},
            "address_detail": {"required": True},
            "zipcode": {"required": True},
            "phone_number": {"required": True},
            "is_default": {"required": True},
        }


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "last_name",
            "role",
        )


class PrivateUserSerializer(ModelSerializer):
    user_addresses = UserAddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "role",
            "email",
            "following",
            "is_deleted",
            "is_active",
            "date_joined",
            "user_addresses",
        )


class InfluencerSerializer(ModelSerializer):
    class Meta:
        model = Influencer
        fields = ("__all__",)


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ("__all__",)
