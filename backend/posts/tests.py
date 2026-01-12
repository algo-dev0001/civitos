"""
API integration tests for posts and comments.
"""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from posts.models import Post
from comments.models import Comment


class PostAPITestCase(TestCase):
    """Test the Post API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create test posts
        self.post1 = Post.objects.create(
            title="Test Post 1",
            body="This is the body of test post 1."
        )
        self.post2 = Post.objects.create(
            title="Test Post 2",
            body="This is the body of test post 2."
        )
        
        # Create some test comments
        Comment.objects.create(
            text="Great post!",
            author="Alice",
            post=self.post1,
            flagged=False
        )
        Comment.objects.create(
            text="This is spam",
            author="Spammer",
            post=self.post1,
            flagged=True
        )
    
    def test_list_posts(self):
        """Test GET /api/posts/ returns all posts."""
        response = self.client.get('/api/posts/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Check that posts include comments
        post_titles = [post['title'] for post in response.data]
        self.assertIn('Test Post 1', post_titles)
        self.assertIn('Test Post 2', post_titles)
    
    def test_retrieve_post_with_comments(self):
        """Test GET /api/posts/<id>/ returns post with nested comments."""
        response = self.client.get(f'/api/posts/{self.post1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post 1')
        self.assertEqual(len(response.data['comments']), 2)
        
        # Check comments are ordered by created_at
        comments = response.data['comments']
        self.assertEqual(comments[0]['author'], 'Alice')
        self.assertEqual(comments[1]['author'], 'Spammer')
        
        # Check flagged status
        self.assertFalse(comments[0]['flagged'])
        self.assertTrue(comments[1]['flagged'])
    
    def test_retrieve_nonexistent_post(self):
        """Test GET /api/posts/999/ returns 404."""
        response = self.client.get('/api/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentCreationAPITestCase(TestCase):
    """Test comment creation with classification."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.post = Post.objects.create(
            title="Test Post",
            body="This is a test post for comments."
        )
    
    def test_create_safe_comment(self):
        """Test creating a safe comment sets flagged=False."""
        comment_data = {
            'text': 'This is a helpful comment. Thanks!',
            'author': 'Bob'
        }
        
        response = self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], comment_data['text'])
        self.assertEqual(response.data['author'], comment_data['author'])
        self.assertEqual(response.data['post'], self.post.id)
        self.assertFalse(response.data['flagged'])
        
        # Verify in database
        comment = Comment.objects.get(id=response.data['id'])
        self.assertFalse(comment.flagged)
    
    def test_create_comment_with_banned_word_spam(self):
        """Test creating a comment with 'spam' sets flagged=True."""
        comment_data = {
            'text': 'This is spam content!',
            'author': 'Spammer'
        }
        
        response = self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['flagged'])
        
        # Verify in database
        comment = Comment.objects.get(id=response.data['id'])
        self.assertTrue(comment.flagged)
    
    def test_create_comment_with_banned_word_scam(self):
        """Test creating a comment with 'scam' sets flagged=True."""
        comment_data = {
            'text': 'This is a scam!',
            'author': 'BadActor'
        }
        
        response = self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['flagged'])
    
    def test_create_comment_with_banned_word_hate(self):
        """Test creating a comment with 'hate' sets flagged=True."""
        comment_data = {
            'text': 'I hate this article',
            'author': 'Hater'
        }
        
        response = self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['flagged'])
    
    def test_create_comment_with_excessive_caps(self):
        """Test creating a comment with excessive caps sets flagged=True."""
        comment_data = {
            'text': 'THIS IS ALL CAPS AND SHOULD BE FLAGGED',
            'author': 'Shouter'
        }
        
        response = self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['flagged'])
    
    def test_create_comment_with_excessive_punctuation(self):
        """Test creating a comment with excessive punctuation sets flagged=True."""
        comment_data = {
            'text': 'Amazing!!!!!!',
            'author': 'Excitable'
        }
        
        response = self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['flagged'])
    
    def test_create_comment_missing_text(self):
        """Test creating a comment without text returns 400."""
        comment_data = {
            'author': 'Bob'
        }
        
        response = self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_comment_missing_author(self):
        """Test creating a comment without author returns 400."""
        comment_data = {
            'text': 'This is a comment'
        }
        
        response = self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_comment_on_nonexistent_post(self):
        """Test creating a comment on non-existent post returns 404."""
        comment_data = {
            'text': 'This is a comment',
            'author': 'Bob'
        }
        
        response = self.client.post(
            '/api/posts/999/comments/',
            comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_flagged_field_readonly(self):
        """Test that flagged field cannot be set directly by client."""
        comment_data = {
            'text': 'This is a safe comment',
            'author': 'Bob',
            'flagged': True  # Try to force flagged=True
        }
        
        response = self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Should be False because classifier determined it's safe
        self.assertFalse(response.data['flagged'])
    
    def test_comments_count_increases(self):
        """Test that adding comments increases the post's comment count."""
        initial_response = self.client.get(f'/api/posts/{self.post.id}/')
        initial_count = len(initial_response.data['comments'])
        
        # Add a comment
        comment_data = {
            'text': 'New comment',
            'author': 'Charlie'
        }
        self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            comment_data,
            format='json'
        )
        
        # Check count increased
        updated_response = self.client.get(f'/api/posts/{self.post.id}/')
        updated_count = len(updated_response.data['comments'])
        self.assertEqual(updated_count, initial_count + 1)

