from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ocr import views

urlpatterns = [
    path(r'img', views.read_image),
]
