from django.urls import path

from . import views


urlpatterns = [
    path("", views.ArticleListAPIView.as_view(), name="article_list"),
    path('<int:pk>', views.ArticleDetailAPIView.as_view(), name='article-detail'),
    # path("<int:pk>", views.ProductDetailAPIView.as_view(), name="article_detail"),
]