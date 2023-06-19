from django.db import models
from common.models import CommonModel


class ChattingRoom(CommonModel):
    """ChattingRoom Model Definition"""

    users = models.ManyToManyField(
        "users.User",
    )

    def other_users(self, user):
        return self.users.exclude(pk=user.pk)

    def __str__(self):
        other_users = self.other_users(self.users.first())
        usernames = ", ".join([user.username for user in other_users])
        return f"Chat with: {usernames}"


class Message(CommonModel):

    """Message Model Definition"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
        related_name="direct_messages",
    )

    def __str__(self) -> str:
        return f"{self.user} :{self.text}"
