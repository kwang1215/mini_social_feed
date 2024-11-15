from django.core.exceptions import ValidationError
from django.db import models
from hitcount.models import HitCount
from hitcount.views import HitCountMixin

from accounts.models import User


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def clean(self):
        if " " in self.name or any(char in self.name for char in "#@!$%^&*()"):
            raise ValidationError(
                "해시태그는 띄어쓰기와 특수문자를 포함할 수 없습니다."
            )


class ArticleType(models.IntegerChoices):
    FACEBOOK = (1, "facebook")
    TWITTER = (2, "twitter")
    INSTAGRAM = (3, "instagram")
    THREADS = (4, "threads")


class ArticleTypeModel(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)

    class Meta:
        db_table = "article_type_model"


class Article(models.Model, HitCountMixin):
    type = models.ForeignKey(
        "ArticleTypeModel",
        db_column="type",
        related_name="articles",
        on_delete=models.CASCADE,
        null=True,
    )
    title = models.CharField(max_length=50)
    content = models.TextField()
    hashtags = models.ManyToManyField(Hashtag, related_name="articles", blank=True)
    view_count = models.PositiveIntegerField(blank=True, default=0)
    likes = models.ManyToManyField(User, related_name="likes_articles", blank=True)
    like_count = models.PositiveIntegerField(blank=True, default=0)
    shares = models.ManyToManyField(User, related_name="shares_articles", blank=True)
    share_count = models.PositiveIntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User:{self.title}"

    def increase_view_count(self, request):
        hit_count = HitCount.objects.get_for_object(self)
        hit_count.hits += 1
        hit_count.save()
        self.view_count = hit_count.hits
        self.save()

    def like_article(self, user):
        if not self.likes.filter(id=user.id).exists():
            self.likes.add(user)
            self.like_count += 1
            self.save()

    def unlike_article(self, user):
        if self.likes.filter(id=user.id).exists():
            self.likes.remove(user)
            self.like_count -= 1
            self.save()

    def share_article(self, user):
        if not self.shares.filter(id=user.id).exists():
            self.shares.add(user)
            self.share_count += 1
            self.save()

    def unshare_article(self, user):
        if self.shares.filter(id=user.id).exists():
            self.shares.remove(user)
            self.share_count -= 1
            self.save()
