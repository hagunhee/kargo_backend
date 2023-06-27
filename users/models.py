from utils import HashidHandler
from django.db import models
from django.apps import apps
from django.contrib.auth.models import AbstractUser  # Custom User Model
from common.models import CommonModel
from products.models import ProductPost


class User(CommonModel, AbstractUser):
    class GradeChoices(models.TextChoices):
        BRONZE = ("bronze", "Bronze")
        SILVER = ("silver", "Silver")
        GOLD = ("gold", "Gold")
        PLATINUM = ("platinum", "Platinum")
        DIAMOND = ("diamond", "Diamond")

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
    # 회원이 일정 점수마다 등급이 올라가는 것을 구현하기 위해 필요한 필드
    score = models.IntegerField(default=0)
    grade = models.CharField(
        max_length=20,
        choices=GradeChoices.choices,
        default=GradeChoices.BRONZE,
    )
    birth = models.DateField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    last_sale = models.DateTimeField(null=True, blank=True)
    login_count = models.IntegerField(default=0)
    sale_count = models.IntegerField(default=0)
    sale_amount = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            self._create_role_specific_instance()
            self._create_basket_instance()

    def _create_role_specific_instance(self):
        if self.role == User.RoleKindChoices.INFLUENCER:
            self._create_influencer_instance()
        elif self.role == User.RoleKindChoices.BRAND:
            self._create_brand_instance()

    def _create_influencer_instance(self):
        influencer = Influencer.objects.create(user=self)
        hashid_handler = HashidHandler()
        influencer.influencer_code = hashid_handler.encode_hash(influencer.pk)
        influencer.save()

    def _create_brand_instance(self):
        brand = Brand.objects.create(user=self)
        brand.save()

    def _create_basket_instance(self):
        basket = apps.get_model("baskets", "Basket").objects.create(user=self)
        basket.save()


class UserAddress(CommonModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_addresses",
    )
    shippingTitle = models.CharField(max_length=100)
    shippingCountryCode = models.CharField(max_length=100)
    shippingPhonePrefix = models.CharField(max_length=100)
    shippingPhone = models.CharField(max_length=100)
    shippingZipcode = models.CharField(max_length=100)
    shippingCountry = models.CharField(max_length=100)
    shippingCity = models.CharField(max_length=100)
    shippingState = models.CharField(max_length=100)
    shippingAddress = models.CharField(max_length=100)
    shippingAddressSub = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)


class Influencer(CommonModel):
    class FeeGradeChoices(models.IntegerChoices):
        BRONZE = 10
        SILVER = 20
        GOLD = 30

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="influencers",
        limit_choices_to={"role": "influencer"},
    )
    shop_name = models.CharField(max_length=100, unique=True)
    # influencerPosting을 통해 연결된 포스트들을 가져올 수 있다.
    product_posts = models.ManyToManyField(
        ProductPost,
        through="InfluencerPosting",
        related_name="influencers",
    )
    fee_grade = models.IntegerField(
        choices=FeeGradeChoices.choices,
        default=FeeGradeChoices.BRONZE,
    )
    account_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    bank_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    account_holder = models.CharField(max_length=100, unique=True, null=True, blank=True)
    influencer_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    sell_count = models.IntegerField(default=0)
    sell_amount = models.IntegerField(default=0)

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


# 해당 인플루언서가 얼마만큼의


class Brand(CommonModel):
    ##유저 아이디를 FK로 받아온다.
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="brands",
        limit_choices_to={"role": "brand"},
    )
    is_approved = models.BooleanField(default=False)
    name = models.CharField(max_length=100, unique=True)
    bank_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    acount_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    account_holder = models.CharField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # 카테고리에서 FK로 받아온다.
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        related_name="brands",
        null=True,
    )

    def __str__(self):
        return self.name


class Business(CommonModel):
    class GradeChoices(models.TextChoices):
        BRONZE = "bronze", "bronze"
        SILVER = "silver", "silver"
        GOLD = "gold", "gold"

    company_name = models.CharField(max_length=100, unique=True)
    fax_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    contact_name = models.CharField(max_length=100, unique=True)
    contact_number = models.CharField(max_length=100, unique=True)
    # 사업자 번호
    business_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    bank_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    acount_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    account_holder = models.CharField(max_length=100, unique=True, null=True, blank=True)
    service = models.CharField(max_length=100, unique=True)
    grade = models.CharField(max_length=20, choices=GradeChoices.choices)
    is_approved = models.BooleanField(default=False)


class BusinessQna(CommonModel):
    business = models.ForeignKey("users.Business", on_delete=models.CASCADE, related_name="qnas")
    title = models.CharField(max_length=200)
    content = models.TextField()
    # Sent, Delivered, Failed, Clicked etc.
    status = models.CharField(max_length=20)
    # 읽었는지 확인하며 시간을 기록한다.
    is_deleted = models.BooleanField(default=False)
    # 메세지를 불러오며 읽었는지 확인한다.
    answer_manager = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="businessqna_answer_manager"
    )

    def __str__(self):
        pass


class UserQna(CommonModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="qnas")
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    # Sent, Delivered, Failed, Clicked etc.
    status = models.CharField(max_length=20)
    # 읽었는지 확인하며 시간을 기록한다.
    is_deleted = models.BooleanField(default=False)
    # 메세지를 불러오며 읽었는지 확인한다.
    answer_manager = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="userqna_answer_manager"
    )

    def __str__(self):
        pass
