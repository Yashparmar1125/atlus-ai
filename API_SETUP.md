# ATLUS API Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file:

```env
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True
OPENROUTER_API_KEY=your-api-key-here
SECRET_KEY=your-secret-key-here
```

### 3. Run the API Server

```bash
python run_api.py
```

Or:

```bash
python -m app.server
```

The API will be available at `http://localhost:5000`

## API Structure

```
app/
├── api/
│   ├── __init__.py          # API initialization
│   ├── chat.py              # Chat endpoint
│   ├── schemas.py           # Pydantic schemas
│   ├── validators.py        # Request validation
│   ├── errors.py            # Error handling
│   └── middleware.py       # Middleware (CORS, logging, rate limiting)
├── server.py                # Flask app factory
└── config.py                # Configuration classes
```

## Features Implemented

### ✅ Industry Best Practices

1. **Application Factory Pattern** - Clean app initialization
2. **Blueprint Architecture** - Modular endpoint organization
3. **Request Validation** - Pydantic schema validation
4. **Error Handling** - Consistent error responses
5. **Middleware** - CORS, logging, security headers
6. **Rate Limiting** - Per-IP request limiting
7. **Request Tracking** - X-Request-ID header support
8. **Health Checks** - Health endpoint for monitoring
9. **API Documentation** - Self-documenting endpoints
10. **Configuration Management** - Environment-based config

### Security Features

- CORS support
- Security headers (X-Content-Type-Options, X-Frame-Options, etc.)
- Request size limits (16MB max)
- Rate limiting
- Input validation

### Logging

- Request/response logging
- Execution time tracking
- Error logging with stack traces
- Request ID correlation

## Testing the API

### Using cURL

```bash
# Health check
curl http://localhost:5000/api/v1/health

# Chat request
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: test-123" \
  -d '{
    "message": "Build a REST API with authentication"
  }'
```

### Using Python

```python
import requests

response = requests.post(
    'http://localhost:5000/api/v1/chat',
    json={'message': 'Build a REST API'},
    headers={'X-Request-ID': 'my-request'}
)

print(response.json())
```

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app.server:create_app()"
```

### Using Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.server:create_app()"]
```

### Environment Variables for Production

```env
FLASK_ENV=production
SECRET_KEY=<strong-random-secret>
OPENROUTER_API_KEY=<your-key>
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/docs` | API documentation |
| POST | `/api/v1/chat` | Process user message |

## Next Steps

1. Add authentication (API keys, JWT)
2. Add database for session management
3. Add Redis for distributed rate limiting
4. Add monitoring/APM integration
5. Add OpenAPI/Swagger documentation
6. Add request/response caching
7. Add WebSocket support for streaming

