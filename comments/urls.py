
from django.urls import path, include
from comments import views

urlpatterns = [
    path(r'review', views.comments),
    path(r'mypage', views.mypage),
]