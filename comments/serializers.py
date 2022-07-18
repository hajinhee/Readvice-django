from rest_framework import serializers

from books.serializers import BookSerializer
from users.serializers import UserSerializer
from .models import Comment as comment


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = comment
        fields = '__all__'
