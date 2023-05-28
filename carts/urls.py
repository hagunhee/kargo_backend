from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>", views.CartDetail.as_view(), name="like"),
    path("items/<int:cart_item_pk>", views.CartItemDetail.as_view()),
]
