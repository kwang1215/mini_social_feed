from django.urls import path

from . import views


urlpatterns = [
    path("", views.ArticleListAPIView.as_view(), name="article_list"),
    path('<int:pk>', views.ArticleDetailAPIView.as_view(), name='article_detail'),
    path('<str:article_type>/likes/<int:pk>', views.ArticleLikeAPIView.as_view(), name='article_like'),
    path('<str:article_type>/share/<int:pk>', views.ArticleShareAPIView.as_view(), name='article_share'),
    # path("<int:pk>", views.ProductDetailAPIView.as_view(), name="article_detail"),
]