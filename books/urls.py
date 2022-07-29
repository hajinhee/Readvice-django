from django.urls import path, include
from books import views

urlpatterns = [
    path(r'search', views.search),
    path(r'upload', views.upload_files)
]