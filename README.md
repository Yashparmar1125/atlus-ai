# ATLUS - Agentic AI Assistant System

<div align="center">

**A production-ready, multi-stage LLM pipeline for intelligent task processing**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**ATLUS** is an advanced agentic AI system that processes user requests through a sophisticated multi-stage pipeline. Unlike simple chatbots, ATLUS uses a structured approach: **Intent Extraction → Planning → Reasoning → Verification → Refactoring → Final Writing**.

The system is designed with production-grade practices, including comprehensive logging, error handling, request validation, and a RESTful API interface.

### Key Highlights

- 🧠 **Multi-Stage Processing**: Breaks down complex tasks into structured steps
- 🔄 **Self-Verification**: Built-in critique and refinement mechanisms
- 🛡️ **Production-Ready**: Error handling, logging, rate limiting, and security
- 🔌 **RESTful API**: Industry-standard Flask API with full documentation
- 📊 **Comprehensive Logging**: Detailed execution tracking and debugging
- ✅ **Type Safety**: Pydantic validation and type checking throughout

---

## ✨ Features

### Core Capabilities

1. **Intent Extraction** - Parses user requests into structured goals, constraints, and expected outputs
2. **Intelligent Planning** - Generates actionable, ordered execution plans
3. **Step-by-Step Reasoning** - Produces comprehensive draft solutions
4. **Self-Verification** - Identifies issues and suggests improvements
5. **Automatic Refinement** - Improves drafts based on verification feedback
6. **Polished Output** - Generates clean, user-facing final responses

### Technical Features

- ✅ **Multi-LLM Pipeline** - Specialized models for each stage
- ✅ **Error Recovery** - Automatic retry and repair mechanisms
- ✅ **Request Validation** - Pydantic schema validation
- ✅ **Rate Limiting** - Per-IP request throttling
- ✅ **Security Headers** - CORS, XSS protection, content-type validation
- ✅ **Request Tracking** - X-Request-ID correlation
- ✅ **Health Checks** - Monitoring-ready endpoints
- ✅ **Comprehensive Logging** - File and console logging with rotation

---

## 🏗️ Architecture

### System Flow

```
User Input
    ↓
Intent Extraction (Structured JSON)
    ↓
Planning (Ordered Steps)
    ↓
Reasoning (Comprehensive Draft)
    ↓
Verification (Issues & Fixes)
    ↓
Refactoring (Improved Draft)
    ↓
Final Writing (Polished Response)
    ↓
Response
```

### Component Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Flask API Layer                       │
│  (Request Validation, Error Handling, Rate Limiting)   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    Agent Orchestrator                    │
│  (Intent → Plan → Reasoning → Verify → Refactor → Write)│
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼──────┐ ┌───▼────────┐
│  LLM Router  │ │ Prompts │ │  Parsers   │
│  (Factory)   │ │         │ │ Validators │
└──────────────┘ └─────────┘ └────────────┘
        │
┌───────▼───────────────────────────────────┐
│         Specialized LLM Instances          │
│  Intent | Planning | Reasoning | Verify    │
│  Writer                                      │
└────────────────────────────────────────────┘
```

### LLM Pipeline

| Stage | LLM | Purpose | Reasoning |
|-------|-----|---------|-----------|
| Intent | `IntentLLM` | Extract structured intent | ❌ |
| Planning | `PlannerLLM` | Generate execution plan | ✅ |
| Reasoning | `ReasoningLLM` | Step-by-step solution | ✅ |
| Verification | `VerifierLLM` | Critique and validate | ✅ |
| Writing | `WriterLLM` | Final polished output | ❌ |

**Provider**: OpenRouter API (free tier models)

---

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager
- OpenRouter API key ([Get one here](https://openrouter.ai/))

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd ATLUS
```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

Create a `.env` file in the project root:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your-api-key-here

# Flask Configuration (Optional)
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False

# Security (Required for Production)
SECRET_KEY=your-secret-key-here

# Logging (Optional)
LOG_LEVEL=INFO
```

---

## ⚡ Quick Start

### Option 1: Run as Python Script

```bash
python run.py
```

This will process a test message and display the result.

### Option 2: Run as API Server

```bash
python run_api.py
```

The API will be available at `http://localhost:5000`

### Test the API

```bash
# Health check
curl http://localhost:5000/api/v1/health

# Chat request
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Build a REST API with authentication"}'
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENROUTER_API_KEY` | OpenRouter API key | - | ✅ Yes |
| `FLASK_ENV` | Environment (development/production/testing) | development | No |
| `FLASK_HOST` | Server host | 0.0.0.0 | No |
| `FLASK_PORT` | Server port | 5000 | No |
| `FLASK_DEBUG` | Enable debug mode | False | No |
| `SECRET_KEY` | Flask secret key | dev-secret-key | ⚠️ Production |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | INFO | No |
| `RATE_LIMIT_ENABLED` | Enable rate limiting | true | No |
| `RATE_LIMIT_REQUESTS` | Max requests per window | 100 | No |
| `RATE_LIMIT_WINDOW` | Time window in seconds | 60 | No |

### Model Configuration

Edit `app/llm/config.py` to customize LLM models, temperatures, and token limits.

---

## 📖 Usage

### Python API

```python
from app.agent.agent import Agent

# Initialize agent
agent = Agent()

# Process request
response = agent.run("Build a web application with authentication")
print(response)
```

### REST API

#### Chat Endpoint

```bash
POST /api/v1/chat
Content-Type: application/json

{
  "message": "Your request here",
  "session_id": "optional-session-id",
  "metadata": {}
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "response": "Agent-generated response...",
    "session_id": "optional-session-id",
    "execution_time": 45.23,
    "request_id": "req_1234567890"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Health Check

```bash
GET /api/v1/health
```

#### API Documentation

```bash
GET /api/v1/docs
```

### Python Client Example

```python
import requests

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
    print(f"Execution time: {data['data']['execution_time']}s")
else:
    print(f"Error: {data['error']['message']}")
```

---

## 📚 API Documentation

Full API documentation is available at:

- **Interactive Docs**: `http://localhost:5000/api/v1/docs`
- **Documentation File**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/api/v1/health` | Health check |
| `GET` | `/api/v1/docs` | API documentation |
| `POST` | `/api/v1/chat` | Process user message |

### Error Codes

| Code | Description | Status |
|------|-------------|--------|
| `INVALID_REQUEST` | Invalid request format | 400 |
| `INVALID_JSON` | Invalid JSON in body | 400 |
| `VALIDATION_ERROR` | Request validation failed | 400 |
| `MESSAGE_TOO_LONG` | Message exceeds max length | 400 |
| `RATE_LIMIT_EXCEEDED` | Too many requests | 429 |
| `INTERNAL_ERROR` | Server error | 500 |

---

## 📁 Project Structure

```
ATLUS/
│
├── app/                          # Main application package
│   ├── agent/                    # Agent orchestration
│   │   └── agent.py             # Core agent logic
│   │
│   ├── api/                      # Flask API layer
│   │   ├── chat.py              # Chat endpoint
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── validators.py        # Request validation
│   │   ├── errors.py            # Error handling
│   │   └── middleware.py       # Middleware (CORS, logging, etc.)
│   │
│   ├── llm/                      # LLM layer
│   │   ├── base.py              # Base LLM interface
│   │   ├── router.py            # LLM factory/router
│   │   ├── config.py            # Model configurations
│   │   ├── intent_llm.py        # Intent extraction LLM
│   │   ├── planner_llm.py       # Planning LLM
│   │   ├── reasoning_llm.py     # Reasoning LLM
│   │   ├── verifier_llm.py      # Verification LLM
│   │   └── writer_llm.py        # Writing LLM
│   │
│   ├── prompts/                  # Prompt builders
│   │   ├── intent_prompt.py     # Intent extraction prompts
│   │   ├── planner_prompt.py    # Planning prompts
│   │   ├── reasoning_prompt.py  # Reasoning prompts
│   │   ├── verifier_prompt.py   # Verification prompts
│   │   ├── refactor_prompt.py   # Refactoring prompts
│   │   └── writer_prompt.py     # Writing prompts
│   │
│   ├── utils/                    # Utilities
│   │   ├── logger.py            # Logging configuration
│   │   ├── parsers/             # Output parsers
│   │   │   ├── json_parser.py  # JSON parsing
│   │   │   └── plan_parser.py  # Plan parsing
│   │   └── validators/          # Validators
│   │       ├── intent_validator.py
│   │       └── plan_validator.py
│   │
│   ├── server.py                # Flask app factory
│   └── config.py                # Application configuration
│
├── tests/                        # Test suite
│   ├── test_intent_llm.py
│   ├── test_planning_llm.py
│   ├── test_reasoning_llm.py
│   ├── test_verifier_llm.py
│   ├── test_writer_llm.py
│   └── conftest.py
│
├── logs/                         # Log files (auto-generated)
│   └── atlus.log
│
├── data/                         # Data directory (for future use)
├── models/                       # Model files (for future use)
├── scripts/                      # Utility scripts
│
├── requirements.txt              # Python dependencies
├── run.py                        # CLI runner
├── run_api.py                    # API server runner
│
├── README.md                     # This file
├── AECHITECTURE.md               # Architecture documentation
├── API_DOCUMENTATION.md          # API reference
├── API_SETUP.md                  # API setup guide
├── CODEBASE_ANALYSIS.md          # Codebase analysis
├── LOGGING_GUIDE.md              # Logging documentation
└── PROMPT_IMPROVEMENTS.md        # Prompt engineering notes
```

---

## 🛠️ Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks (if configured)
pre-commit install
```

### Code Style

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to all functions and classes
- Keep functions focused and small

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_intent_llm.py

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes with tests
3. Update documentation
4. Submit pull request

---

## 🧪 Testing

### Test Structure

```
tests/
├── test_intent_llm.py      # Intent LLM unit tests
├── test_planning_llm.py    # Planning LLM unit tests
├── test_reasoning_llm.py   # Reasoning LLM unit tests
├── test_verifier_llm.py    # Verifier LLM unit tests
├── test_writer_llm.py      # Writer LLM unit tests
└── conftest.py             # Shared test fixtures
```

### Running Tests

```bash
# All tests
pytest

# Specific test
pytest tests/test_intent_llm.py::TestIntentLLM::test_generate_success

# With verbose output
pytest -v

# With coverage
pytest --cov=app --cov-report=term-missing
```

All tests use mocked LLM responses - no API calls are made during testing.

---

## 🚢 Deployment

### Development Server

```bash
python run_api.py
```

### Production with Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app.server:create_app()"
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.server:create_app()"]
```

### Production Checklist

- [ ] Set `SECRET_KEY` environment variable
- [ ] Set `FLASK_ENV=production`
- [ ] Configure HTTPS (use reverse proxy like nginx)
- [ ] Set up monitoring and alerting
- [ ] Configure log rotation
- [ ] Set up rate limiting (Redis for distributed)
- [ ] Add authentication/authorization
- [ ] Configure CORS for specific origins
- [ ] Set up database for session management
- [ ] Configure backup and recovery

---

## 📊 Logging

All operations are logged to `logs/atlus.log` with rotation support.

### Log Levels

- **DEBUG**: Detailed debugging information
- **INFO**: General informational messages
- **WARNING**: Warning messages
- **ERROR**: Error messages with stack traces

### Viewing Logs

```bash
# Tail logs
tail -f logs/atlus.log

# Search for errors
grep ERROR logs/atlus.log

# View recent activity
tail -n 100 logs/atlus.log
```

See [LOGGING_GUIDE.md](LOGGING_GUIDE.md) for detailed logging documentation.

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'app'`

**Solution**: Run from project root directory or add to PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### 2. API Key Not Found

**Problem**: `OPENROUTER_API_KEY` not set

**Solution**: Create `.env` file with your API key:
```env
OPENROUTER_API_KEY=your-key-here
```

#### 3. Port Already in Use

**Problem**: Port 5000 already in use

**Solution**: Change port:
```bash
export FLASK_PORT=5001
python run_api.py
```

#### 4. Empty Responses

**Problem**: Agent returns empty or minimal responses

**Solution**: 
- Check logs for errors
- Verify API key is valid
- Check model availability on OpenRouter
- Review prompt outputs in logs

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Update documentation
5. Submit a pull request

### Development Guidelines

- Write tests for new features
- Follow existing code style
- Add docstrings to new functions
- Update README if needed
- Keep commits atomic and well-described

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **OpenRouter** - For providing LLM API access
- **Flask** - Web framework
- **Pydantic** - Data validation
- **OpenAI** - Python SDK

---

## 📞 Support

For issues, questions, or contributions:

- Open an issue on GitHub
- Check existing documentation
- Review logs for debugging information

---

## 🗺️ Roadmap

### Planned Features

- [ ] Session management and conversation history
- [ ] Long-term memory with vector database
- [ ] Tool integration (Python execution, RAG)
- [ ] WebSocket support for streaming responses
- [ ] Authentication and authorization
- [ ] Distributed rate limiting with Redis
- [ ] OpenAPI/Swagger documentation
- [ ] Response caching
- [ ] Metrics and monitoring integration

---

## 📈 Performance

### Typical Execution Times

- Intent Extraction: ~2-3 seconds
- Planning: ~2-3 seconds
- Reasoning: ~10-15 seconds
- Verification: ~5-8 seconds
- Refactoring: ~10-15 seconds
- Final Writing: ~2-3 seconds

**Total**: ~30-45 seconds per request

*Times vary based on model availability and request complexity*

---

## 🔐 Security

### Current Security Features

- ✅ Request validation
- ✅ Rate limiting
- ✅ Security headers
- ✅ Input sanitization
- ✅ Error message sanitization

### Production Security Recommendations

- Use HTTPS (TLS/SSL)
- Implement API authentication
- Restrict CORS origins
- Use environment variables for secrets
- Regular security audits
- Monitor for suspicious activity

---

<div align="center">

**Built with ❤️ using Python, Flask, and OpenRouter**

[Report Bug](https://github.com/your-repo/issues) · [Request Feature](https://github.com/your-repo/issues) · [Documentation](API_DOCUMENTATION.md)

</div>



