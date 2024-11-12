from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

# class LikeAPIView(APIView):
#     serializer_class = ProductListSerializer
#     permission_classes = [IsAuthenticated]

#     # [찜하기 및 취소] 이미 찜한 경우 취소, 그렇지 않으면 찜하기 처리
#     def post(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)

#         # 이미 찜한 제품이면 찜하기 취소
#         if request.user in product.likes.all():
#             product.likes.remove(request.user)
#             return Response({"message": "찜하기 취소했습니다."}, status=200)

#         # 찜하기 추가
#         product.likes.add(request.user)
#         return Response({"message": "찜하기 했습니다."}, status=200)