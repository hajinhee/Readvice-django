
from django.urls import path, include
from comments import views

urlpatterns = [
    path(r'write', views.write),
    path(r'mypage', views.mypage),
    path(r'myinfo', views.all_info),
]