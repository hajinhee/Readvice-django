from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['book_img', 'book_title']

