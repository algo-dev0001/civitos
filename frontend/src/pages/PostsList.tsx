/**
 * PostsList Page
 * 
 * Displays a list of all blog posts.
 */

import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/client';
import type { Post } from '../types/api';

export default function PostsList() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setLoading(true);
        const data = await api.getPosts();
        setPosts(data);
        setError(null);
      } catch (err) {
        setError('Failed to load posts. Make sure the backend is running on http://localhost:8000');
        console.error('Error fetching posts:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading posts...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="container">
      <h1>Blog Posts</h1>
      
      {posts.length === 0 ? (
        <p>No posts available. Create some posts in the Django admin!</p>
      ) : (
        <div className="posts-list">
          {posts.map((post) => (
            <article key={post.id} className="post-card">
              <h2>
                <Link to={`/posts/${post.id}`}>{post.title}</Link>
              </h2>
              <p className="post-body">{post.body}</p>
              <div className="post-meta">
                <span className="comment-count">
                  {post.comments.length} comment{post.comments.length !== 1 ? 's' : ''}
                </span>
                {post.comments.some(c => c.flagged) && (
                  <span className="flagged-indicator">
                    ⚠️ {post.comments.filter(c => c.flagged).length} flagged
                  </span>
                )}
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
