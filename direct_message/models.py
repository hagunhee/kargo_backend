from django.db import models
from common.models import CommonModel


class Message(CommonModel):

    """Message Model Definition"""

    message = models.TextField()
    sender = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    receiver = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self) -> str:
        return f"{self.user} :{self.text}"
