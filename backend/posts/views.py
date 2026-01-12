"""
API views for the posts app.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from comments.models import Comment
from comments.serializers import CommentSerializer
from classifier import classify_comment


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Post model.
    
    Provides:
    - GET /api/posts/ - List all posts
    - GET /api/posts/<id>/ - Retrieve a post with comments
    - POST /api/posts/<id>/comments/ - Add a comment to a post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    @action(detail=True, methods=['post'], url_path='comments')
    def add_comment(self, request, pk=None):
        """
        Add a comment to a post.
        
        Automatically classifies the comment and sets the flagged field.
        """
        post = self.get_object()
        
        # Create serializer with incoming data
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            # Get the comment text for classification
            comment_text = serializer.validated_data.get('text', '')
            
            # Classify the comment
            needs_review = classify_comment(comment_text)
            
            # Save the comment with the post and flagged status
            comment = serializer.save(post=post, flagged=needs_review)
            
            # Return the created comment
            return Response(
                CommentSerializer(comment).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

