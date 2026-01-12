/**
 * PostDetail Page
 * 
 * Displays a single post with its comments and a form to add new comments.
 */

import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api/client';
import type { Post, Comment } from '../types/api';

export default function PostDetail() {
  const { id } = useParams<{ id: string }>();
  const [post, setPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Form state
  const [author, setAuthor] = useState('');
  const [text, setText] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPost = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        const data = await api.getPost(parseInt(id));
        setPost(data);
        setError(null);
      } catch (err) {
        setError('Failed to load post. Make sure the backend is running.');
        console.error('Error fetching post:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!post || !author.trim() || !text.trim()) return;

    try {
      setSubmitting(true);
      setSubmitError(null);
      
      const newComment = await api.addComment(post.id, {
        author: author.trim(),
        text: text.trim(),
      });

      // Update post with new comment
      setPost({
        ...post,
        comments: [...post.comments, newComment],
      });

      // Reset form
      setAuthor('');
      setText('');
    } catch (err) {
      setSubmitError('Failed to add comment. Please try again.');
      console.error('Error adding comment:', err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading post...</div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="container">
        <div className="error">{error || 'Post not found'}</div>
        <Link to="/">← Back to posts</Link>
      </div>
    );
  }

  return (
    <div className="container">
      <Link to="/" className="back-link">← Back to posts</Link>
      
      <article className="post-detail">
        <h1>{post.title}</h1>
        <div className="post-body">{post.body}</div>
      </article>

      <section className="comments-section">
        <h2>Comments ({post.comments.length})</h2>

        {post.comments.length === 0 ? (
          <p className="no-comments">No comments yet. Be the first to comment!</p>
        ) : (
          <div className="comments-list">
            {post.comments.map((comment: Comment) => (
              <div
                key={comment.id}
                className={`comment ${comment.flagged ? 'flagged' : ''}`}
              >
                {comment.flagged && (
                  <div className="flagged-badge">⚠️ Flagged for review</div>
                )}
                <div className="comment-author">{comment.author}</div>
                <div className="comment-text">{comment.text}</div>
                <div className="comment-date">
                  {new Date(comment.created_at).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        )}

        <form onSubmit={handleSubmit} className="comment-form">
          <h3>Add a Comment</h3>
          
          {submitError && (
            <div className="error">{submitError}</div>
          )}

          <div className="form-group">
            <label htmlFor="author">Name</label>
            <input
              id="author"
              type="text"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
              placeholder="Your name"
              required
              disabled={submitting}
            />
          </div>

          <div className="form-group">
            <label htmlFor="text">Comment</label>
            <textarea
              id="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Share your thoughts..."
              rows={4}
              required
              disabled={submitting}
            />
          </div>

          <button type="submit" disabled={submitting}>
            {submitting ? 'Submitting...' : 'Post Comment'}
          </button>
        </form>
      </section>
    </div>
  );
}
