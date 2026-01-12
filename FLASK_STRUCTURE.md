# ATLUS Flask Application Structure

## Overview
Industry-standard Flask application structure with clean separation of concerns.

## Directory Structure

```
app/
├── __init__.py              # Package initialization, exports create_app
├── server.py                # Application factory and root routes
├── config.py                # Configuration classes (Dev, Prod, Test)
│
├── api/                     # API Layer
│   ├── __init__.py         # API initialization
│   └── v1/                 # API Version 1
│       ├── __init__.py     # V1 registration
│       ├── routes/         # Route handlers (blueprints)
│       │   ├── __init__.py # Routes registration
│       │   ├── chat.py     # Chat endpoints
│       │   └── health.py   # Health check endpoints
│       ├── schemas.py      # Pydantic request/response models
│       ├── validators.py   # Request validation logic
│       └── errors.py       # Error handlers and custom exceptions
│
├── core/                    # Core Components
│   ├── __init__.py
│   ├── middleware.py        # Request/response middleware
│   └── extensions.py        # Flask extensions (CORS, etc.)
│
├── services/                # Business Logic Layer
│   ├── __init__.py
│   ├── chat_service.py      # Chat business logic
│   └── health_service.py    # Health check logic
│
└── utils/                   # Utilities (Flask-specific)
    ├── logger.py            # Logging configuration
    ├── parsers/             # Response parsers
    └── validators/          # Data validators
```

## Key Concepts

### 1. Application Factory Pattern
- `create_app()` function in `server.py`
- Allows multiple instances with different configs
- Testable and production-ready

### 2. Blueprint-Based Routing
- Each feature has its own blueprint
- Routes organized by version (`api/v1/`)
- Easy to add new versions (`api/v2/`)

### 3. Layered Architecture

#### API Layer (`api/v1/routes/`)
- Thin controllers
- Handle HTTP concerns only
- Validate requests
- Return responses

#### Service Layer (`services/`)
- Contains business logic
- Independent of HTTP
- Reusable across different interfaces

#### Core Layer (`core/`)
- Cross-cutting concerns
- Middleware
- Extensions
- Configuration

### 4. Separation of Concerns

**Routes** (`api/v1/routes/*.py`):
```python
@chat_bp.route("/chat", methods=["POST"])
def chat():
    payload = validate_request(ChatRequestSchema, request)
    result = ChatService.process_chat(payload, request_id)
    return jsonify(response), 200
```

**Services** (`services/*.py`):
```python
class ChatService:
    @classmethod
    def process_chat(cls, payload, request_id):
        # Business logic here
        orchestrator = cls._get_orchestrator()
        response = orchestrator.run(payload["message"])
        return {"response": response, ...}
```

## File Responsibilities

### `server.py`
- Create Flask app
- Load configuration
- Initialize extensions
- Register API
- Root routes

### `api/v1/__init__.py`
- Register all v1 components
- Wire up routes, errors, middleware

### `api/v1/routes/*.py`
- Define endpoint blueprints
- Handle HTTP requests
- Validate input
- Call services
- Format responses

### `core/middleware.py`
- Request logging
- Request ID tracking
- Rate limiting
- Security headers
- Response time tracking

### `core/extensions.py`
- Initialize Flask extensions
- CORS configuration
- Other third-party integrations

### `services/*.py`
- Business logic
- Orchestrator integration
- Data processing
- Validation rules

### `api/v1/schemas.py`
- Pydantic models
- Request/response validation
- API contracts

### `api/v1/errors.py`
- Custom exceptions
- Error handlers
- Error response formatting

## Benefits

### ✅ Scalability
- Easy to add new endpoints
- Version API independently
- Modular components

### ✅ Maintainability
- Clear file organization
- Single responsibility
- Easy to locate code

### ✅ Testability
- Services can be tested independently
- Mock orchestrator easily
- Unit test routes separately

### ✅ Industry Standard
- Follows Flask best practices
- Similar to Django, FastAPI patterns
- Easy for new developers

## Usage

### Running the Server

```bash
# Development
python run_api.py

# Or directly
python app/server.py
```

### Adding a New Endpoint

1. **Create route file**: `app/api/v1/routes/new_feature.py`
```python
from flask import Blueprint
new_feature_bp = Blueprint("new_feature", __name__)

@new_feature_bp.route("/feature", methods=["POST"])
def feature_endpoint():
    # Implementation
    pass
```

2. **Register blueprint**: Update `app/api/v1/routes/__init__.py`
```python
from app.api.v1.routes.new_feature import new_feature_bp

def register_routes(app):
    app.register_blueprint(chat_bp, url_prefix="/api/v1")
    app.register_blueprint(new_feature_bp, url_prefix="/api/v1")
```

3. **Add schema**: Update `app/api/v1/schemas.py`
```python
class NewFeatureRequest(BaseModel):
    data: str
```

4. **Add service**: Create `app/services/new_feature_service.py`
```python
class NewFeatureService:
    @classmethod
    def process(cls, data):
        # Business logic
        return result
```

## Migration from Old Structure

### Before
```
app/
├── api/
│   └── chat.py              # Routes + Middleware mixed
├── llm/                     # Core AI logic (moved to root)
├── agent/                   # Core AI logic (moved to root)
```

### After
```
Root level:                  # Core AI Logic
├── orchestrator/
├── agent/
├── llm/
├── prompts/
├── utils/

app/                         # Flask API Only
├── api/v1/routes/           # Clean route separation
├── core/                    # Middleware separate
├── services/                # Business logic
```

## Best Practices

1. **Keep routes thin**: Delegate to services
2. **Use type hints**: All functions typed
3. **Validate early**: At API boundary
4. **Log appropriately**: Use structured logging
5. **Handle errors gracefully**: Custom error handlers
6. **Document endpoints**: Docstrings on routes
7. **Version APIs**: `/api/v1/`, `/api/v2/`
8. **Test thoroughly**: Unit + integration tests

## Next Steps

1. Add authentication middleware
2. Implement proper rate limiting (Redis)
3. Add API documentation (Swagger/OpenAPI)
4. Add request/response logging
5. Implement caching layer
6. Add metrics and monitoring


