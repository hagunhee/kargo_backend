from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>", views.BasketDetail.as_view(), name="like"),
    path("items/<int:basket_item_pk>", views.BasketItemDetail.as_view()),
]
