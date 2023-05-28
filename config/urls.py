from django.contrib import admin
from django.urls import path, include
from users import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("likes/", include("carts.likesurls")),
    path("carts/", include("carts.urls")),
    path("influencers/", include("users.sellersurls")),
]
