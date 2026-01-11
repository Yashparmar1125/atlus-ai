# ATLUS API Documentation

## Overview

The ATLUS API provides a RESTful interface to the ATLUS agent system. It follows industry best practices including request validation, error handling, logging, and security headers.

## Base URL

```
http://localhost:5000/api/v1
```

## Authentication

Currently, the API does not require authentication. In production, implement API keys or OAuth2.

## Endpoints

### 1. Chat Endpoint

Process user messages and return agent-generated responses.

**Endpoint:** `POST /api/v1/chat`

**Request Headers:**
```
Content-Type: application/json
X-Request-ID: <optional-request-id>
```

**Request Body:**
```json
{
  "message": "I want to build a web application with a database and authentication",
  "session_id": "optional-session-id",
  "metadata": {
    "source": "web",
    "user_id": "user123"
  }
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "data": {
    "response": "Here is a comprehensive solution for building a web application...",
    "session_id": "optional-session-id",
    "execution_time": 45.23,
    "request_id": "req_1234567890"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Response (Error - 400):**
```json
{
  "success": false,
  "error": {
    "message": "message field is required and cannot be empty",
    "code": "INVALID_REQUEST",
    "status": 400
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "req_1234567890"
}
```

**Error Codes:**
- `INVALID_REQUEST` (400): Invalid request format
- `INVALID_JSON` (400): Invalid JSON in request body
- `VALIDATION_ERROR` (400): Request validation failed
- `MESSAGE_TOO_LONG` (400): Message exceeds maximum length
- `RATE_LIMIT_EXCEEDED` (429): Too many requests
- `INTERNAL_ERROR` (500): Internal server error

### 2. Health Check

Check API health status.

**Endpoint:** `GET /api/v1/health`

**Response (200):**
```json
{
  "status": "healthy",
  "service": "atlus-api",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 3. API Documentation

Get API documentation.

**Endpoint:** `GET /api/v1/docs`

**Response (200):**
```json
{
  "title": "ATLUS Agent API",
  "version": "1.0.0",
  "description": "AI Agent API for intelligent task processing",
  "endpoints": { ... }
}
```

## Request Validation

### Message Requirements
- **Required:** Yes
- **Type:** String
- **Min Length:** 1 character
- **Max Length:** 5000 characters
- **Cannot be:** Empty or whitespace only

### Optional Fields
- `session_id`: String identifier for session tracking
- `metadata`: Object with additional context

## Response Headers

All responses include:
- `X-Request-ID`: Request identifier for tracking
- `X-Process-Time`: Processing time in seconds
- `Access-Control-Allow-Origin`: CORS header
- Security headers (X-Content-Type-Options, X-Frame-Options, etc.)

## Rate Limiting

Default rate limits:
- **Max Requests:** 100 per window
- **Window:** 60 seconds
- **Per IP:** Rate limiting is per client IP

When rate limit is exceeded, returns `429 Too Many Requests` with error code `RATE_LIMIT_EXCEEDED`.

## Error Handling

All errors follow a consistent format:

```json
{
  "success": false,
  "error": {
    "message": "Human-readable error message",
    "code": "ERROR_CODE",
    "status": 400,
    "details": []  // Optional validation details
  },
  "timestamp": "ISO 8601 timestamp",
  "request_id": "request-identifier"
}
```

## Examples

### cURL

```bash
# Chat request
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Build a REST API with authentication"
  }'

# Health check
curl http://localhost:5000/api/v1/health
```

### Python

```python
import requests

# Chat request
response = requests.post(
    'http://localhost:5000/api/v1/chat',
    json={
        'message': 'Build a REST API with authentication',
        'session_id': 'session123'
    },
    headers={'X-Request-ID': 'my-request-id'}
)

data = response.json()
if data['success']:
    print(data['data']['response'])
else:
    print(f"Error: {data['error']['message']}")
```

### JavaScript

```javascript
// Chat request
fetch('http://localhost:5000/api/v1/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Request-ID': 'my-request-id'
  },
  body: JSON.stringify({
    message: 'Build a REST API with authentication',
    session_id: 'session123'
  })
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log(data.data.response);
  } else {
    console.error('Error:', data.error.message);
  }
});
```

## Best Practices

1. **Always include X-Request-ID** for request tracking
2. **Handle rate limits** with exponential backoff
3. **Validate responses** before processing
4. **Use session_id** for conversation tracking
5. **Monitor execution_time** for performance

## Production Considerations

1. **Enable HTTPS** - Use reverse proxy (nginx) with SSL
2. **Add Authentication** - Implement API keys or OAuth2
3. **Use Redis** - For distributed rate limiting
4. **Add Monitoring** - Integrate with APM tools
5. **Set SECRET_KEY** - Use strong secret key in production
6. **Configure CORS** - Restrict allowed origins
7. **Add Logging** - Centralized logging system
8. **Use Gunicorn** - Production WSGI server

## Running the Server

### Development
```bash
python run_api.py
```

### Production (with Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app.server:create_app()"
```

## Environment Variables

- `FLASK_ENV`: Environment (development, production, testing)
- `FLASK_HOST`: Host to bind to (default: 0.0.0.0)
- `FLASK_PORT`: Port to bind to (default: 5000)
- `FLASK_DEBUG`: Enable debug mode (default: False)
- `SECRET_KEY`: Flask secret key (required in production)
- `LOG_LEVEL`: Logging level (default: INFO)
- `RATE_LIMIT_ENABLED`: Enable rate limiting (default: true)
- `RATE_LIMIT_REQUESTS`: Max requests per window (default: 100)
- `RATE_LIMIT_WINDOW`: Time window in seconds (default: 60)

