"""
Script to test the API endpoints.
"""

import json
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from posts.models import Post
from comments.models import Comment
from posts.views import PostViewSet
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request


def test_api_endpoints():
    """Test all API endpoints."""
    
    # Clear existing test data
    Comment.objects.all().delete()
    Post.objects.all().delete()
    
    # Create test posts
    post1 = Post.objects.create(
        title="Introduction to Django",
        body="Django is a great web framework for Python."
    )
    post2 = Post.objects.create(
        title="React Best Practices",
        body="Learn how to write clean React components."
    )
    
    # Create some comments
    Comment.objects.create(
        text="Great article!",
        author="Alice",
        post=post1,
        flagged=False
    )
    Comment.objects.create(
        text="This is spam content",
        author="BadActor",
        post=post1,
        flagged=True
    )
    
    factory = APIRequestFactory()
    viewset = PostViewSet.as_view({'get': 'list'})
    
    print("=" * 60)
    print("Testing API Endpoints")
    print("=" * 60)
    
    # Test 1: GET /api/posts/ - List all posts
    print("\n1. GET /api/posts/ - List all posts")
    request = factory.get('/api/posts/')
    response = viewset(request)
    print(f"   Status: {response.status_code}")
    print(f"   Number of posts: {len(response.data)}")
    print(f"   Posts: {[p['title'] for p in response.data]}")
    
    # Test 2: GET /api/posts/<id>/ - Retrieve a post with comments
    print("\n2. GET /api/posts/1/ - Retrieve post with comments")
    viewset_detail = PostViewSet.as_view({'get': 'retrieve'})
    request = factory.get(f'/api/posts/{post1.id}/')
    response = viewset_detail(request, pk=post1.id)
    print(f"   Status: {response.status_code}")
    print(f"   Post: {response.data['title']}")
    print(f"   Number of comments: {len(response.data['comments'])}")
    print(f"   Comments:")
    for comment in response.data['comments']:
        print(f"      - {comment['author']}: {comment['text'][:30]}... (flagged: {comment['flagged']})")
    
    # Test 3: POST /api/posts/<id>/comments/ - Add a safe comment
    print("\n3. POST /api/posts/1/comments/ - Add a safe comment")
    viewset_comment = PostViewSet.as_view({'post': 'add_comment'})
    comment_data = {
        'text': 'This is a helpful comment. Thanks for sharing!',
        'author': 'Charlie'
    }
    request = factory.post(
        f'/api/posts/{post1.id}/comments/',
        data=json.dumps(comment_data),
        content_type='application/json'
    )
    response = viewset_comment(request, pk=post1.id)
    print(f"   Status: {response.status_code}")
    print(f"   Created comment ID: {response.data.get('id')}")
    print(f"   Author: {response.data.get('author')}")
    print(f"   Flagged: {response.data.get('flagged')}")
    
    # Test 4: POST /api/posts/<id>/comments/ - Add a flagged comment
    print("\n4. POST /api/posts/1/comments/ - Add a comment with banned word")
    comment_data = {
        'text': 'This is spam! Buy now!',
        'author': 'Spammer'
    }
    request = factory.post(
        f'/api/posts/{post1.id}/comments/',
        data=json.dumps(comment_data),
        content_type='application/json'
    )
    response = viewset_comment(request, pk=post1.id)
    print(f"   Status: {response.status_code}")
    print(f"   Created comment ID: {response.data.get('id')}")
    print(f"   Author: {response.data.get('author')}")
    print(f"   Flagged: {response.data.get('flagged')} (should be True)")
    
    # Test 5: POST /api/posts/<id>/comments/ - Add comment with excessive caps
    print("\n5. POST /api/posts/1/comments/ - Add comment with excessive caps")
    comment_data = {
        'text': 'THIS IS ALL CAPS AND SHOULD BE FLAGGED',
        'author': 'Shouter'
    }
    request = factory.post(
        f'/api/posts/{post1.id}/comments/',
        data=json.dumps(comment_data),
        content_type='application/json'
    )
    response = viewset_comment(request, pk=post1.id)
    print(f"   Status: {response.status_code}")
    print(f"   Flagged: {response.data.get('flagged')} (should be True)")
    
    print("\n" + "=" * 60)
    print("✓ All API endpoint tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    test_api_endpoints()
