from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>", views.LikeList.as_view(), name="like"),
    path("<int:pk>/productposts/<int:product_post_pk>", views.LikeToggle.as_view()),
]
