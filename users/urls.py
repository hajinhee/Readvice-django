
from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path(r'join', views.join),
    path(r'login', views.login),
    path(r'logout', views.logout),
]