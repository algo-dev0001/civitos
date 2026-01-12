"""
Serializers for the posts app.
"""

from rest_framework import serializers
from .models import Post
from comments.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model with nested comments.
    
    Comments are read-only and ordered by created_at (oldest first).
    """
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'comments']
        read_only_fields = ['id']
