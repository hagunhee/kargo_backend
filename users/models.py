from django.db import models
from django.contrib.auth.models import AbstractUser  # Custom User Model
from common.models import CommonModel


class User(AbstractUser):
    class RoleKindChoices(models.TextChoices):
        USER = ("user", "User")
        SELLER = ("seller", "Seller")
        BUISNESS = ("buisness", "Buisness")
        BRANDUSER = ("branduser", "Brand User")

    username = models.CharField(max_length=50, default="", unique=True)
    first_name = models.CharField(
        max_length=50,
        editable=False,
    )
    last_name = models.CharField(
        max_length=50,
        editable=False,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        max_length=50,
        choices=RoleKindChoices.choices,
        default=RoleKindChoices.USER,
    )
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True,
    )

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class UserAddress(CommonModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_addresses",
    )
    address = models.CharField(max_length=100)
    address_detail = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
