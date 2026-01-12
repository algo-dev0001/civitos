from django.db import models


class Post(models.Model):
    """Blog post model."""
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']  # Newest posts first
