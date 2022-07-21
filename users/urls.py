
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
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # token/
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # token/refresh/
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify')  # tok

]