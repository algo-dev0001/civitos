from django.db import models
from posts.models import Post


class Comment(models.Model):
    """Comment model with classification flagging."""
    text = models.TextField()
    author = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"

    class Meta:
        ordering = ['created_at']  # Oldest comments first
