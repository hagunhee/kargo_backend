from django.contrib import admin
from django.urls import path, include
from users import views
from strawberry.django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("likes/", include("baskets.likesurls")),
    path("baskets/", include("baskets.urls")),
    path("influencers/", include("users.sellersurls")),
    path("graphql", GraphQLView.as_view(schema=schema, graphiql=True)),
]
