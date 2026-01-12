"""
Management command to seed the database with sample posts and comments.
"""

from django.core.management.base import BaseCommand
from posts.models import Post
from comments.models import Comment


class Command(BaseCommand):
    help = 'Seeds the database with sample posts and comments'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Comment.objects.all().delete()
        Post.objects.all().delete()

        # Create posts
        post1 = Post.objects.create(
            title="Introduction to Django REST Framework",
            body="Django REST Framework (DRF) is a powerful toolkit for building Web APIs. "
                 "It provides features like serialization, authentication, and view sets that make "
                 "API development much easier. In this post, we'll explore the basics of DRF."
        )

        post2 = Post.objects.create(
            title="React Best Practices for 2026",
            body="React continues to evolve with new patterns and best practices. "
                 "In this guide, we'll cover hooks, TypeScript integration, proper component "
                 "composition, and performance optimization techniques."
        )

        post3 = Post.objects.create(
            title="AI-Powered Content Moderation",
            body="Automated content moderation using AI is becoming essential for modern platforms. "
                 "We'll discuss how to implement classification systems that can flag inappropriate "
                 "content while maintaining user experience."
        )

        # Create safe comments
        Comment.objects.create(
            text="Great article! Very informative and well-written.",
            author="Alice",
            post=post1,
            flagged=False
        )

        Comment.objects.create(
            text="Thanks for sharing this. I learned a lot about DRF.",
            author="Bob",
            post=post1,
            flagged=False
        )

        Comment.objects.create(
            text="This is exactly what I needed. The examples are very clear.",
            author="Charlie",
            post=post2,
            flagged=False
        )

        # Create flagged comments (spam)
        Comment.objects.create(
            text="This is spam! Buy now for limited offer!",
            author="Spammer123",
            post=post1,
            flagged=True
        )

        Comment.objects.create(
            text="I hate this article, it's a scam!",
            author="TrollUser",
            post=post2,
            flagged=True
        )

        # Create flagged comment (excessive caps)
        Comment.objects.create(
            text="THIS IS AMAZING EVERYONE SHOULD READ THIS NOW!!!!!!",
            author="ExcitedUser",
            post=post2,
            flagged=True
        )

        Comment.objects.create(
            text="Really helpful content. Looking forward to more posts!",
            author="David",
            post=post3,
            flagged=False
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {Post.objects.count()} posts and '
                f'{Comment.objects.count()} comments '
                f'({Comment.objects.filter(flagged=True).count()} flagged)'
            )
        )
