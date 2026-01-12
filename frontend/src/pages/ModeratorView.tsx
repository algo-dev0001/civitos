/**
 * ModeratorView Page
 * 
 * Displays all flagged comments across all posts for moderation.
 * No authentication required - assumes trusted user.
 */

import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/client';
import type { Post, Comment } from '../types/api';

interface FlaggedCommentWithPost extends Comment {
  postTitle: string;
  postId: number;
}

export default function ModeratorView() {
  const [flaggedComments, setFlaggedComments] = useState<FlaggedCommentWithPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFlaggedComments = async () => {
      try {
        setLoading(true);
        
        // Fetch all posts with comments
        const posts = await api.getPosts();
        
        // Extract flagged comments and add post context
        const flagged: FlaggedCommentWithPost[] = [];
        posts.forEach((post: Post) => {
          post.comments
            .filter((comment) => comment.flagged)
            .forEach((comment) => {
              flagged.push({
                ...comment,
                postTitle: post.title,
                postId: post.id,
              });
            });
        });
        
        // Sort by most recent first
        flagged.sort((a, b) => 
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        
        setFlaggedComments(flagged);
        setError(null);
      } catch (err) {
        setError('Failed to load flagged comments. Make sure the backend is running.');
        console.error('Error fetching flagged comments:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchFlaggedComments();
  }, []);

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading flagged comments...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">{error}</div>
        <Link to="/">← Back to posts</Link>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="moderator-header">
        <h1>🛡️ Moderator View</h1>
        <p>Review flagged comments that need attention</p>
        <Link to="/" className="back-link">← Back to posts</Link>
      </div>

      {flaggedComments.length === 0 ? (
        <div className="moderator-empty">
          <div className="empty-state">
            <span className="empty-icon">✅</span>
            <h2>All clear!</h2>
            <p>No flagged comments require review at this time.</p>
          </div>
        </div>
      ) : (
        <div className="moderator-stats">
          <div className="stat-card">
            <div className="stat-number">{flaggedComments.length}</div>
            <div className="stat-label">Comments flagged</div>
          </div>
        </div>
      )}

      {flaggedComments.length > 0 && (
        <div className="flagged-comments-list">
          {flaggedComments.map((comment) => (
            <div key={comment.id} className="flagged-comment-card">
              <div className="flagged-badge-large">⚠️ Needs review</div>
              
              <div className="comment-context">
                <Link to={`/posts/${comment.postId}`} className="post-link">
                  On post: {comment.postTitle}
                </Link>
              </div>

              <div className="comment-content">
                <div className="comment-author-large">
                  <strong>{comment.author}</strong>
                </div>
                <div className="comment-text-large">{comment.text}</div>
                <div className="comment-date">
                  {new Date(comment.created_at).toLocaleString()}
                </div>
              </div>

              <div className="moderator-actions">
                <Link 
                  to={`/posts/${comment.postId}`}
                  className="view-context-btn"
                >
                  View in context →
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
