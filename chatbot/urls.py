from django.urls import path, include

from chatbot import views

urlpatterns = [
    path(r'chatbot', views.chatbot),

]