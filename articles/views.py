from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ArticleFilter
from .models import Article
from .serializers import (
    ArticleDetailSerializer,
    ArticleLikeSerializer,
    ArticleListSerializer,
    ArticleShareSerializer,
)


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    filterset_class = ArticleFilter


class ArticleDetailAPIView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer

    def get_object(self):
        object = super().get_object()
        object.increase_view_count(self.request)
        return object


class ArticleLikeAPIView(GenericAPIView):
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.perform_act(
            request, act="like", response_status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        return self.perform_act(
            request, act="unlike", response_status=status.HTTP_204_NO_CONTENT
        )

    def perform_act(self, request, act, response_status):
        article = self.get_object()
        serializer = ArticleLikeSerializer(
            article, context={"request": request}, act=act
        )
        return Response(serializer.data, status=response_status)


class ArticleShareAPIView(GenericAPIView):
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.perform_act(
            request, act="share", response_status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        return self.perform_act(
            request, act="unshare", response_status=status.HTTP_204_NO_CONTENT
        )

    def perform_act(self, request, act, response_status):
        article = self.get_object()
        serializer = ArticleShareSerializer(
            article, context={"request": request}, act=act
        )
        return Response(serializer.data, status=response_status)
