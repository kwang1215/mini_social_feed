from rest_framework import serializers

from .models import Article, Hashtag


# [해시태그 시리얼라이저] 해시태그 id, 이름 반환
class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = (
            "id",
            "name",
        )


# [상품 목록] 상품의 주요 정보 반환
class ArticleListSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            "id",
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
class ProductDetailSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(many=True, source="tags", required=False)
    author = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = (
            "id",
            "type",
            "title",
            "content",
            "hashtags",
            "view_count",
            "like_count",
            "share_count",
            "created_at",
            "updated_at",
        )
