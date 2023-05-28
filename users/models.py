import os
from pathlib import Path
import environ
from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import AbstractUser  # Custom User Model
from common.models import CommonModel
from products.models import ProductPost
from hashids import Hashids


env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
salt = env("SALT")


class User(AbstractUser):
    class RoleKindChoices(models.TextChoices):
        USER = ("user", "User")
        INFLUENCER = ("influencer", "Influencer")
        BUISNESS = ("buisness", "Buisness")
        BRAND = ("brand", "Brand")

    username = models.CharField(max_length=50, default="", unique=True)
    first_name = models.CharField(
        max_length=50,
    )
    last_name = models.CharField(
        max_length=50,
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
    mileage = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    

    def save(self, *args, **kwargs):
        # is_new는 현재 인스턴스가 새로 생성되는 것인지 아닌지를 판단하는 변수
        # 새로 생성되는 것이라면 True, 아니라면 False
        # 새로 생성되는 것이라면 Influencer 인스턴스를 생성
        # 이 때 args, kwargs는 save 메서드에 전달되는 인자들
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new and self.role == User.RoleKindChoices.INFLUENCER:
            influencer = Influencer.objects.create(user=self)
            hashids = Hashids(salt=salt, min_length=6)
            influencer.influencer_code = hashids.encode(influencer.pk)
            influencer.save()
        if is_new and self.role == User.RoleKindChoices.BRAND:
            brand = Brand.objects.create(user=self)
            brand.save()


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


class Influencer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="influencers",
        limit_choices_to={"role": "influencer"},
    )
    shop_name = models.CharField(max_length=100, unique=True)
    profile_imageURL = models.URLField(max_length=200, blank=True)
    # influencerPosting을 통해 연결된 포스트들을 가져올 수 있다.
    product_posts = models.ManyToManyField(
        ProductPost,
        through="InfluencerPosting",
        related_name="influencers",
    )

    influencer_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.shop_name


class InfluencerPosting(CommonModel):
    influencer = models.ForeignKey(
        Influencer,
        on_delete=models.CASCADE,
        related_name="influencer_postings",
    )
    product_post = models.ForeignKey(
        ProductPost,
        on_delete=models.CASCADE,
        related_name="influencer_postings",
    )
    is_approved = models.BooleanField(default=True)
    is_posted = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    imageURL = models.URLField(max_length=200, blank=True)
    videoURL = models.URLField(max_length=200, blank=True)


class Brand(CommonModel):
    ##유저 아이디를 FK로 받아온다.
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="brands",
        limit_choices_to={"role": "brand"},
    )

    name = models.CharField(max_length=100, unique=True)
    brand_imageURL = models.ImageField(upload_to="brand_logo", blank=True)
    description = models.TextField(blank=True)
    # 카테고리에서 FK로 받아온다.
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        related_name="brands",
        null=True,
    )

    def __str__(self):
        return self.name
