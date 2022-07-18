from rest_framework import serializers

from books.serializers import BookSerializer
from users.serializers import UserSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['email'] = UserSerializer(read_only=True)
        self.fields['isbn'] = BookSerializer(read_only=True)
        return super(CommentSerializer, self).to_representation(instance)

