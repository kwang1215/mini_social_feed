from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import User


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 해시태그 이름

    def __str__(self):
        return self.name

    def clean(self):
        # [데이터 유효성 검사] 해시태그에 띄어쓰기 또는 특수문자가 포함되지 않도록 설정
        if " " in self.name or any(char in self.name for char in "#@!$%^&*()"):
            raise ValidationError(
                "해시태그는 띄어쓰기와 특수문자를 포함할 수 없습니다."
            )


class Article(models.Model):
    CHOICE_PRODUCT = ["facebook", "twitter", "instagram", "threads"]
    type = models.CharField(max_length=50, choices=CHOICE_PRODUCT, default="type")
    title = models.CharField(max_length=50)
    content = models.TextField()
    hashtags = models.ManyToManyField(Hashtag, related_name="articles", blank=True)
    view_count = models.PositiveIntegerField(blank=True, default=0)
    like_count = models.PositiveIntegerField(blank=True, default=0)
    share_count = models.PositiveIntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User:{self.author} (Status:{self.status})"
