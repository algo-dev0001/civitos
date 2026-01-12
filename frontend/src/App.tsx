/**
 * Main App Component
 * 
 * Sets up routing for the Smart Comments application.
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import PostsList from './pages/PostsList';
import PostDetail from './pages/PostDetail';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <h1>Smart Comments</h1>
          <p>AI-powered comment moderation</p>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<PostsList />} />
            <Route path="/posts/:id" element={<PostDetail />} />
          </Routes>
        </main>

        <footer className="app-footer">
          <p>Built with Django + React + TypeScript</p>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;
