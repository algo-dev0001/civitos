/**
 * API Client for Smart Comments Backend
 * 
 * Provides typed methods for interacting with the Django REST API.
 */

import axios from 'axios';
import type { Post, Comment, CreateCommentData } from '../types/api';

// Base URL for the API - update this if backend runs on different port
const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * API methods for interacting with posts and comments
 */
export const api = {
  /**
   * Get all posts with their comments
   */
  getPosts: async (): Promise<Post[]> => {
    const response = await apiClient.get<Post[]>('/posts/');
    console.log(response.data)
    return response.data;
  },

  /**
   * Get a single post by ID with its comments
   */
  getPost: async (id: number): Promise<Post> => {
    const response = await apiClient.get<Post>(`/posts/${id}/`);
    return response.data;
  },

  /**
   * Add a comment to a post
   * The backend will automatically classify and set the flagged field
   */
  addComment: async (
    postId: number,
    data: CreateCommentData
  ): Promise<Comment> => {
    const response = await apiClient.post<Comment>(
      `/posts/${postId}/comments/`,
      data
    );
    return response.data;
  },
};

export default api;
