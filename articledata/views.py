from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ArticleStatsSerializer


class ArticleStatisticsView(APIView):
    def get(self, request):
        serializer = ArticleStatsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.get_statistics()
        print(request.query_params)
        return Response(data)
