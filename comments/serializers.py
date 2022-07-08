from rest_framework import serializers
from .models import Comment as comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = '__all__'

