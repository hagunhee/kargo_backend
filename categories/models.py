from django.db import models

##패런츠 카테고리 필드를 FK로 설정하여 동일한 테이블내의 다른 카테고리를 부모로 갖을 수 있다.


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
