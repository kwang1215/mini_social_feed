from django.urls import path
from .views import ArticleStatisticsView

urlpatterns = [
    path("", ArticleStatisticsView.as_view(), name='article_stats'),
]
