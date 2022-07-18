from django.urls import path, include
from books import views

urlpatterns = [
    path(r'info', views.info)
]