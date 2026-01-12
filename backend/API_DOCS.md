# API Endpoints Documentation

## Available Endpoints

### 1. List All Posts
**GET** `/api/posts/`

Returns a list of all blog posts with their nested comments.

**Response Example:**
```json
[
  {
    "id": 1,
    "title": "Introduction to Django",
    "body": "Django is a great web framework...",
    "comments": [
      {
        "id": 1,
        "text": "Great article!",
        "author": "Alice",
        "post": 1,
        "created_at": "2026-01-12T12:00:00Z",
        "flagged": false
      }
    ]
  }
]
```

### 2. Retrieve Single Post
**GET** `/api/posts/<id>/`

Returns a specific post with all its comments.

**Response Example:**
```json
{
  "id": 1,
  "title": "Introduction to Django",
  "body": "Django is a great web framework...",
  "comments": [
    {
      "id": 1,
      "text": "Great article!",
      "author": "Alice",
      "post": 1,
      "created_at": "2026-01-12T12:00:00Z",
      "flagged": false
    }
  ]
}
```

### 3. Add Comment to Post
**POST** `/api/posts/<id>/comments/`

Adds a new comment to a specific post. The comment is automatically classified and the `flagged` field is set based on the classification result.

**Request Body:**
```json
{
  "text": "This is my comment",
  "author": "John Doe"
}
```

**Response Example (201 Created):**
```json
{
  "id": 2,
  "text": "This is my comment",
  "author": "John Doe",
  "post": 1,
  "created_at": "2026-01-12T13:00:00Z",
  "flagged": false
}
```

## Classification Rules

Comments are automatically classified when created. A comment will be flagged (`flagged: true`) if:

1. Contains banned words (spam, scam, hate, etc.)
2. Has excessive capitalization (>50% uppercase)
3. Has excessive punctuation (>5 exclamation or question marks)

## Testing the API

### Using curl:

```bash
# List all posts
curl http://localhost:8000/api/posts/

# Get a specific post
curl http://localhost:8000/api/posts/1/

# Add a comment
curl -X POST http://localhost:8000/api/posts/1/comments/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Great post!", "author": "Jane"}'
```

### Using Python requests:

```python
import requests

# List posts
response = requests.get('http://localhost:8000/api/posts/')
print(response.json())

# Add comment
comment_data = {
    "text": "This is a helpful comment",
    "author": "Alice"
}
response = requests.post(
    'http://localhost:8000/api/posts/1/comments/',
    json=comment_data
)
print(response.json())
```

## Admin Interface

Access the Django admin at: http://localhost:8000/admin/

Create a superuser first:
```bash
python manage.py createsuperuser
```
