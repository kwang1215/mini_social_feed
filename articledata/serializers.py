from datetime import timedelta

from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import serializers

from articles.models import Article



class ArticleStatsSerializer(serializers.Serializer):
    hashtag = serializers.CharField(required=False, allow_blank=True)
    query_type = serializers.ChoiceField(choices=["date", "hour"], default="date")
    start = serializers.DateField(required=False)
    end = serializers.DateField(required=False)
    value = serializers.ChoiceField(
        choices=["count", "view_count", "like_count", "share_count"], default="count"
    )

    def get_statistics(self):
        hashtag = self.validated_data.get("hashtag")
        query_type = self.validated_data.get("query_type")
        start = self.validated_data.get("start")
        end = self.validated_data.get("end")
        value = self.validated_data.get("value")

        today = timezone.now().date()

        if not start:
            start = today - timedelta(days=7 if query_type == "hour" else 30)
        if not end:
            end = today

        queryset = Article.objects.filter(updated_at__date__range=[start, end])

        if hashtag:
            queryset = queryset.filter(hashtags__name=hashtag)

        if value == "count":
            if query_type == "date":
                return (
                    queryset.extra(select={"day": "DATE(updated_at)"})
                    .values("day")
                    .annotate(total=Count("id"))
                )
            elif query_type == "hour":
                return (
                    queryset.extra(
                        select={
                            "hour": "DATE_FORMAT(updated_at, '%%Y-%%m-%%d %%H:00:00')"
                        }
                    )
                    .values("hour")
                    .annotate(total=Count("id"))
                )
        elif value in ["view_count", "like_count", "share_count"]:
            if query_type == "date":
                return (
                    queryset.extra(select={"day": "DATE(updated_at)"})
                    .values("day")
                    .annotate(total=Sum(value))
                )
            elif query_type == "hour":
                return (
                    queryset.extra(
                        select={
                            "hour": "DATE_FORMAT(updated_at, '%%Y-%%m-%%d %%H:00:00')"
                        }
                    )
                    .values("hour")
                    .annotate(total=Sum(value))
                )
        else:
            raise ValueError("Invalid value parameter")
