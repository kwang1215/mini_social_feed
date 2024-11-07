from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView

from . import views

urlpatterns = [
    path("signup", views.UserCreateView.as_view(), name="user-signup"),
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout", TokenBlacklistView.as_view(), name="logout"),
]