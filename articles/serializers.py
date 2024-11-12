from rest_framework import serializers

from .models import Hashtag, Article


# [해시태그 시리얼라이저] 해시태그 id, 이름 반환
class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = (
            "id",
            "name",
        )


# [상품 목록] 상품의 주요 정보 반환
class ProductListSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(many=True, source="tags", required=False)
    author = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = (
            "id",
            "type",
            "title",
            "hashtags",
            "view_count",
            "like_count",
            "share_count",
            "created_at",
            "updated_at",
        )


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
