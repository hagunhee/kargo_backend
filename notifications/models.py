from django.db import models
from common.models import CommonModel


class Notification(CommonModel):
    title = models.CharField(max_length=200)
    message = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Sent, Delivered, Failed, Clicked etc.
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Notification for {self.user.username} sent at {self.timestamp}"
