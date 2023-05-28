from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

# 토큰은 헤더에 키:Authorization 밸류: Token xxxxxxxxxxxxxxxxxx 라는 규칙으로 보내야한다.
urlpatterns = [
    path("", views.Me.as_view()),
]
