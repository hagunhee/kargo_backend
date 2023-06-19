from django.db import models
from common.models import CommonModel
from django.utils import timezone


class Notification(CommonModel):
    title = models.CharField(max_length=200)
    message = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Sent, Delivered, Failed, Clicked etc.
    status = models.CharField(max_length=20)
    # 읽었는지 확인하며 시간을 기록한다.
    read_at = models.DateTimeField(blank=True, null=True)

    # 메세지를 불러오며 읽었는지 확인한다.
    def get_message(self):
        self.read_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Notification for {self.user.username} sent at {self.timestamp}"


class Notice(CommonModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # 공지가 몇월 몇일까지 유효한지
    valid_until = models.DateTimeField()
    # Sent, Delivered, Failed, Clicked etc.
    status = models.CharField(max_length=20)
    # 읽었는지 확인하며 시간을 기록한다.
    is_deleted = models.BooleanField(default=False)
    # 메세지를 불러오며 읽었는지 확인한다.

    def __str__(self):
        pass
