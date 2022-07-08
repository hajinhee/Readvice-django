
from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path(r'join', views.users),
    path(r'login', views.login),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # token/
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # token/refresh/
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify')  # tok

]