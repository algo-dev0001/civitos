"""
Serializers for the comments app.
"""

from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model with all fields."""
    
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at', 'flagged']
        read_only_fields = ['id', 'created_at', 'flagged', 'post']  # post is set by the view
