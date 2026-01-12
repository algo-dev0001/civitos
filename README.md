# Smart Comments System

A full-stack blog platform with AI-powered comment moderation built with Django REST Framework and React + TypeScript.

## ✨ Features

- 🤖 **AI-Powered Classification**: Optional OpenAI integration for nuanced content moderation
- 🛡️ **Rule-Based Fallback**: Always-available pattern matching for banned words
- ⚡ **Real-Time Moderation**: Comments auto-flagged on submission
- � **Moderator View**: Dedicated interface for reviewing flagged content
- 🐳 **Docker Ready**: Complete containerization setup
- ✅ **Comprehensive Tests**: 42 tests with 100% pass rate

## �🏗️ Architecture Overview

### Backend (Django REST Framework)
- **Framework**: Django 5.2 + Django REST Framework
- **Database**: SQLite (dev), PostgreSQL-ready for production
- **API Design**: RESTful endpoints with nested resources
- **Key Endpoints**:
  - `GET /api/posts/` - List all posts
  - `GET /api/posts/{id}/` - Get post with comments
  - `POST /api/posts/{id}/comments/` - Add comment (auto-classified)

### Frontend (React + TypeScript)
- **Framework**: React 18 with TypeScript for type safety
- **Build Tool**: Vite for fast development and optimized builds
- **Routing**: React Router for client-side navigation
- **API Client**: Axios with environment-aware URLs
- **Pages**:
  - `/` - Posts list with preview
  - `/posts/:id` - Post detail with comments
  - `/moderator` - Flagged comments review (bonus feature)

### Classification System

The platform supports **dual classification modes** with automatic fallback:

#### 🤖 AI-Based (Optional)
```python
# Uses OpenAI GPT-4o-mini for context-aware moderation
classify_comment_ai(text: str) -> bool
```

**Features**:
- Context-aware detection (understands sarcasm, nuance)
- Multi-language support
- ~500ms latency, ~$0.0002 per comment
- Requires OpenAI API key

#### 🛡️ Rule-Based (Default)
```python
# Pattern matching for banned words and heuristics
classify_comment_rule_based(text: str) -> bool
```

**Features**:
- Banned words detection
- Excessive caps (>50% uppercase)
- Excessive punctuation (>5 marks)
- <1ms latency, zero cost
- No external dependencies

**Why Dual Mode?**
1. **AI**: Nuanced, context-aware, handles edge cases
2. **Rules**: Fast, reliable, works offline as fallback
3. **Graceful Degradation**: System never fails if AI is unavailable
4. **Cost Control**: Use AI only when needed

**See [AI_CLASSIFIER.md](backend/AI_CLASSIFIER.md) for complete documentation.**

## 🚀 Running Locally

### Option 1: Development Mode (Recommended for development)

**Backend** (Terminal 1):
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs at `http://127.0.0.1:8000`

**Optional - Enable AI Classification**:
```bash
# Add to your environment or .env file
export USE_AI_CLASSIFIER=True
export OPENAI_API_KEY='sk-...'
```

**Frontend** (Terminal 2):
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

### Option 2: Docker (Production-like)

```bash
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

See [DOCKER.md](DOCKER.md) for detailed Docker documentation.

## 🧪 Testing

Run the comprehensive test suite (42 tests):

```bash
cd backend
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

**Test Coverage**:
- ✅ 13 rule-based classifier tests
- ✅ 11 AI classifier tests (with mocking)
- ✅ 4 fallback mechanism tests
- ✅ 14 API integration tests

All tests pass with proper error handling and fallback verification.

## 📈 Scaling Strategies

### 1. Asynchronous Processing
**Problem**: Blocking API calls for expensive operations  
**Solution**: Use Celery + Redis for background tasks

```python
@shared_task
def classify_comment_async(comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.flagged = ml_classifier.predict(comment.text)
    comment.save()
```

**Benefits**:
- Non-blocking API responses
- Retry failed classifications
- Horizontal scaling of workers

### 2. ML-Based Classification
**Current**: Rule-based (fast, transparent)  
**Future**: Fine-tuned transformer model

```python
from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert"
)

def classify_comment_ml(text: str) -> bool:
    result = classifier(text)[0]
    return result['label'] == 'toxic' and result['score'] > 0.7
```

**Benefits**:
- Context-aware detection
- Multi-language support
- Continuous improvement with feedback

### 3. Authentication & Authorization
**Add User Roles**:
- `User`: Can post comments
- `Moderator`: Can review/approve flagged comments
- `Admin`: Full access

```python
from rest_framework.permissions import IsAuthenticated

class ModeratorOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'moderator'
```

### 4. Database Optimization
- **Indexing**: Add indexes on `post_id`, `created_at`, `flagged`
- **Caching**: Redis cache for frequently accessed posts
- **Read Replicas**: Separate read/write databases
- **Pagination**: Limit query results (already implemented in DRF)

### 5. Infrastructure
- **Load Balancer**: Nginx/HAProxy for multiple app servers
- **CDN**: CloudFlare for static assets
- **Monitoring**: Sentry for errors, Prometheus for metrics
- **Auto-scaling**: Kubernetes for container orchestration

## 🎯 Improvements with More Time

### High Priority
1. **Comment Moderation Actions**: Approve/reject buttons in moderator view
2. **User Authentication**: JWT tokens with Django SimpleJWT
3. **Real ML Model**: Fine-tune BERT on hate speech dataset
4. **Pagination**: Implement on frontend for large post lists
5. **Search**: Full-text search on posts/comments with PostgreSQL

### Medium Priority
6. **Rate Limiting**: Prevent spam with Django Ratelimit
7. **Email Notifications**: Alert moderators of flagged comments
8. **Comment Editing**: Allow users to edit within 5 minutes
9. **Rich Text**: Markdown support for post bodies
10. **Analytics Dashboard**: Metrics on flagged comments, trends

### Nice to Have
11. **Real-time Updates**: WebSocket for live comment feeds
12. **Multi-language**: i18n for internationalization
13. **Accessibility**: ARIA labels, keyboard navigation
14. **Mobile App**: React Native with shared API
15. **A/B Testing**: Experiment with different classification thresholds

## 📁 Project Structure

```
assessment/
├── backend/                 # Django REST API
│   ├── config/             # Django settings
│   ├── posts/              # Posts app (models, views, serializers)
│   ├── comments/           # Comments app (models, serializers)
│   ├── classifier/         # Classification logic
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # React + TypeScript
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── pages/         # Route components
│   │   ├── types/         # TypeScript interfaces
│   │   ├── App.tsx        # Main app with routing
│   │   └── main.tsx       # Entry point
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml      # Container orchestration
├── DOCKER.md              # Docker documentation
└── README.md              # This file
```

## 🔧 Technology Choices

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Backend Framework** | Django REST Framework | Batteries-included, great ORM, admin panel |
| **Frontend Framework** | React + TypeScript | Component reusability, type safety |
| **Database** | SQLite → PostgreSQL | Easy local dev, production-ready migration |
| **Classification** | Rule-based | Fast, transparent, no training data needed |
| **API Design** | REST | Simple, well-understood, good tooling |
| **Testing** | Django TestCase | Built-in, comprehensive, fast |
| **Containerization** | Docker + Compose | Consistent environments, easy deployment |

## 📝 API Documentation

### Get All Posts
```http
GET /api/posts/
```

**Response**:
```json
[
  {
    "id": 1,
    "title": "First Post",
    "body": "Post content...",
    "comments": [
      {
        "id": 1,
        "text": "Great post!",
        "author": "Alice",
        "created_at": "2026-01-12T10:00:00Z",
        "flagged": false
      }
    ]
  }
]
```

### Add Comment
```http
POST /api/posts/{id}/comments/
Content-Type: application/json

{
  "text": "This is my comment",
  "author": "Bob"
}
```

**Response**:
```json
{
  "id": 2,
  "text": "This is my comment",
  "author": "Bob",
  "created_at": "2026-01-12T10:05:00Z",
  "flagged": false,
  "post": 1
}
```

## 🤝 Contributing

This is a hiring challenge submission. For production use, consider:
- Adding proper authentication
- Implementing rate limiting
- Using a production WSGI server (Gunicorn)
- Setting up CI/CD pipeline
- Adding monitoring and logging

## 📄 License

MIT License - feel free to use for learning purposes.

---

**Built with ❤️ as a hiring challenge to demonstrate full-stack skills, API design, and production mindset.**
