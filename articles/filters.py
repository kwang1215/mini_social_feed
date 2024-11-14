from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Article, ArticleType


class ArticleFilter(filters.FilterSet):
    hashtag = filters.CharFilter(field_name="hashtags__name", lookup_expr="exact")
    type = filters.ChoiceFilter(choices=ArticleType.choices, field_name="type", lookup_expr="exact")
    search = filters.CharFilter(method="filter_search")
    order_by = filters.OrderingFilter(
        fields=["created_at", "updated_at", "like_count", "share_count", "view_count"]
    )


    class Meta:
        model = Article
        fields = ["hashtag", "type"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            (
                Q(title__icontains=value) | Q(content__icontains=value)
            )
        )
