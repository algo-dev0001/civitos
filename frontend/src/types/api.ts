/**
 * TypeScript types for the Smart Comments API
 */

export interface Comment {
  id: number;
  text: string;
  author: string;
  post: number;
  created_at: string;
  flagged: boolean;
}

export interface Post {
  id: number;
  title: string;
  body: string;
  comments: Comment[];
}

export interface CreateCommentData {
  text: string;
  author: string;
}
