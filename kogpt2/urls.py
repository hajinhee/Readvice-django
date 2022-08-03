from django.urls import path, include

from kogpt2 import views

urlpatterns = [
    path(r'generate', views.generate),
]
