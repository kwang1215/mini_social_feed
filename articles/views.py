from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ArticleFilter
from .models import Article
from .serializers import ArticleListSerializer


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    filterset_class = ArticleFilter



class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)

        # 이미 좋아요한 경우 삭제, 그렇지 않으면 추가
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            # message = "찜하기 취소했습니다."
        else:
            article.likes.add(request.user)
            # message = "찜하기 했습니다."

        return Response({"message": message}, status=200)
