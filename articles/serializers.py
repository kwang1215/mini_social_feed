from django.db import models
from hitcount.models import HitCount
from rest_framework import serializers

from .models import Article, Hashtag


# [해시태그 시리얼라이저] 해시태그 id, 이름 반환
class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("name",)


# [상품 목록] 상품의 주요 정보 반환
class ArticleListSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            "id",
            "type",
            "title",
            "content",
            "created_at",
            "updated_at",
            "like_count",
            "share_count",
            "view_count",
        )

    def get_content(self, obj):
        return obj.content[:20]


# [상품 상세 시리얼라이저] 상품의 상세 정보와 리뷰 정보 반환
class ArticleDetailSerializer(serializers.ModelSerializer):
    hashtags = HashtagSerializer(many=True)

    class Meta:
        model = Article
        fields = "__all__"


class ArticleLikeSerializer(serializers.ModelSerializer):
    act_message = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["act_message"]

    def __init__(self, *args, **kwargs):
        self.act = kwargs.pop("act")
        super().__init__(*args, **kwargs)

    def get_act_message(self, article):
        act = self.act
        user = self.context["request"].user

        if act == "like":
            article.like_article(user)
            return f"https://www.{article.type.name}.com/likes/{article.id}"
        else:
            article.unlike_article(user)
            return f"https://www.{article.type.name}.com/unlikes/{article.id}"


class ArticleShareSerializer(serializers.ModelSerializer):
    act_message = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["act_message"]

    def __init__(self, *args, **kwargs):
        self.act = kwargs.pop("act")
        super().__init__(*args, **kwargs)

    def get_act_message(self, article):
        act = self.act
        user = self.context["request"].user

        if act == "share":
            article.share_article(user)
            return f"https://www.{article.type.name}.com/share/{article.id}"
        else:
            article.unshare_article(user)
            return f"https://www.{article.type.name}.com/unshare/{article.id}"
