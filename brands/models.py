from django.db import models
from common.models import CommonModel


class Brand(CommonModel):
    ##유저 아이디를 FK로 받아온다.
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="brands",
    )

    name = models.CharField(max_length=100, unique=True)
    imageURL = models.ImageField(upload_to="brand_logo", blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
