/**
 * Main App Component
 * 
 * Sets up routing for the Smart Comments application.
 */

import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import PostsList from './pages/PostsList';
import PostDetail from './pages/PostDetail';
import ModeratorView from './pages/ModeratorView';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <div className="header-content">
            <div>
              <h1>Smart Comments</h1>
              <p>AI-powered comment moderation</p>
            </div>
            <nav className="header-nav">
              <Link to="/" className="nav-link">Posts</Link>
              <Link to="/moderator" className="nav-link moderator-link">
                🛡️ Moderator
              </Link>
            </nav>
          </div>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<PostsList />} />
            <Route path="/posts/:id" element={<PostDetail />} />
            <Route path="/moderator" element={<ModeratorView />} />
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
