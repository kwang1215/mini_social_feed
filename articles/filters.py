from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Article


class ArticleFilter(filters.FilterSet):
    hashtag = filters.CharFilter(field_name="hashtags__name", lookup_expr="exact")
    type = filters.CharFilter(field_name="type", lookup_expr="exact")
    search_by = filters.CharFilter(method="filter_search_by")
    order_by = filters.OrderingFilter(
        fields=["created_at", "updated_at", "like_count", "share_count", "view_count"]
    )

    class Meta:
        model = Article
        fields = ["hashtag", "type"]

    def filter_search_by(self, queryset, name, value):
        search_fields = self.request.query_params.get("search_by", "title,content").split(",")
        query = Q()
        
        for field in search_fields:
            query |= Q(**{f"{field}__icontains": value})
        
        return queryset.filter(query)
