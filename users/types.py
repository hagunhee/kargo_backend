import strawberry
from strawberry import auto
from . import models


@strawberry.django.type(models.UserAddress)
class UserAddressType:
    id: auto
    shippingTitle: auto
    shippingCountryCode: auto
    shippingPhonePrefix: auto
    shippingPhone: auto
    shippingZipcode: auto
    shippingCountry: auto
    shippingCity: auto
    shippingState: auto
    shippingAddress: auto
    shippingAddressSub: auto
    is_default: auto


@strawberry.django.type(models.Influencer)
class InfluencerType:
    id: auto
    user: auto
    shop_name: auto
    profile_imageURL: auto
    product_posts: auto
    fee_grade: auto
    account_number: auto
    bank_name: auto
    account_holder: auto
    influencer_code: auto
    is_approved: auto
    sell_count: auto
    sell_amount: auto
    created_at: auto
    updated_at: auto


@strawberry.django.type(models.InfluencerPosting)
class InfluencerPostingType:
    id: auto
    influencer: auto
    product_post: auto
    is_approved: auto
    is_posted: auto
    is_deleted: auto
    description: auto
    imgURL: auto
    videoURL: auto
    created_at: auto
    updated_at: auto


@strawberry.django.type(models.Brand)
class BrandType:
    user: auto
    is_approved: auto
    name: auto
    bank_name: auto
    acount_number: auto
    account_holder: auto
    brand_imageURL: auto
    description: auto
    category: auto
    created_at: auto
    updated_at: auto


@strawberry.django.type(models.Business)
class BusinessType:
    id: auto
    company_name: auto
    contact_number: auto
    contact_name: auto
    fax_number: auto
    business_number: auto
    bank_name: auto
    acount_number: auto
    account_holder: auto
    service: auto
    grade: auto
    is_approved: auto
    created_at: auto
    updated_at: auto


@strawberry.django.type(models.BusinessQna)
class BusinessQnaType:
    id: auto
    business: auto
    title: auto
    content: auto
    status: auto
    is_deleted: auto
    created_at: auto
    updated_at: auto


@strawberry.django.type(models.UserQna)
class UserQnaType:
    id: auto
    user: auto
    title: auto
    subject: auto
    content: auto
    imgURL: auto
    status: auto
    is_deleted: auto
    answer_manager: auto


@strawberry.django.type(models.User)
class UserType:
    id: auto
    username: auto
    first_name: auto
    last_name: auto
    email: auto
    role: auto
    following: auto
    mileage: auto
    is_deleted: auto
    is_active: auto
    score: auto
    grade: auto
    birth: auto
    last_login: auto
    last_sale: auto
    login_count: auto
    sale_count: auto
    sale_amount: auto
    created_at: auto
    updated_at: auto
    user_addresses: auto
    influencers: auto
    brands: auto
