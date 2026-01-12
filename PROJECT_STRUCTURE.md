# ATLUS Project Structure

## 📁 Complete Directory Tree

```
ATLUS/
│
├── 📦 ROOT LEVEL (Core AI Logic)
│   │
│   ├── orchestrator/              # 🎯 Request Routing
│   │   ├── __init__.py
│   │   └── orchestrator.py        # Intent classification & agent selection
│   │
│   ├── agent/                     # 🤖 Agent Implementations  
│   │   ├── __init__.py
│   │   ├── simple_agent.py        # Quick responses (greetings, etc.)
│   │   └── task_agent.py          # Complex task pipeline
│   │
│   ├── llm/                       # 🧠 LLM Interfaces
│   │   ├── __init__.py
│   │   ├── base.py                # Abstract LLM interface
│   │   ├── config.py              # Model configurations
│   │   ├── router.py              # LLM factory pattern
│   │   ├── intent_llm.py          # Intent extraction
│   │   ├── planner_llm.py         # Planning
│   │   ├── reasoning_llm.py       # Reasoning
│   │   ├── verifier_llm.py        # Verification
│   │   ├── writer_llm.py          # Final writing
│   │   └── chat_llm.py            # Simple chat
│   │
│   ├── prompts/                   # 📝 Prompt Builders
│   │   ├── __init__.py
│   │   ├── classifier_prompt.py   # Intent classification
│   │   ├── intent_prompt.py       # Intent extraction
│   │   ├── planner_prompt.py      # Planning
│   │   ├── reasoning_prompt.py    # Reasoning
│   │   ├── verifier_prompt.py     # Verification
│   │   ├── refactor_prompt.py     # Refactoring
│   │   ├── writer_prompt.py       # Final writing
│   │   └── chat_prompt.py         # Simple chat
│   │
│   └── utils/                     # 🛠️ Core Utilities
│       ├── __init__.py
│       ├── logger.py              # Logging configuration
│       ├── parsers/               # Output parsers
│       │   ├── json_parser.py
│       │   └── plan_parser.py
│       └── validators/            # Data validators
│           ├── classifier_validator.py
│           ├── intent_validator.py
│           └── plan_validator.py
│
├── 🌐 APP (Flask API)
│   │
│   ├── app/
│   │   ├── __init__.py            # Package initialization
│   │   ├── server.py              # Application factory
│   │   ├── config.py              # Configuration classes
│   │   │
│   │   ├── api/                   # 🔌 API Layer
│   │   │   ├── __init__.py        # API initialization
│   │   │   └── v1/                # API Version 1
│   │   │       ├── __init__.py    # V1 registration
│   │   │       ├── routes/        # Route handlers
│   │   │       │   ├── __init__.py
│   │   │       │   ├── chat.py    # Chat endpoint
│   │   │       │   └── health.py  # Health endpoint
│   │   │       ├── schemas.py     # Pydantic models
│   │   │       ├── validators.py  # Request validation
│   │   │       └── errors.py      # Error handling
│   │   │
│   │   ├── core/                  # ⚙️ Core Components
│   │   │   ├── __init__.py
│   │   │   ├── middleware.py      # Request/response middleware
│   │   │   └── extensions.py      # Flask extensions (CORS)
│   │   │
│   │   ├── services/              # 💼 Business Logic
│   │   │   ├── __init__.py
│   │   │   ├── chat_service.py    # Chat business logic
│   │   │   └── health_service.py  # Health check logic
│   │   │
│   │   └── utils/                 # 🔧 Flask Utilities
│   │       ├── __init__.py
│   │       ├── logger.py          # Logging
│   │       ├── parsers/           # Response parsers
│   │       └── validators/        # Data validators
│   │
│   ├── run_api.py                 # API server runner
│   └── run.py                     # CLI runner
│
├── 🧪 TESTS
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_intent_llm.py
│   │   ├── test_planning_llm.py
│   │   ├── test_reasoning_llm.py
│   │   ├── test_verifier_llm.py
│   │   └── test_writer_llm.py
│   └── run_tests.py
│
├── 📊 DATA & MODELS
│   ├── data/                      # Data storage
│   ├── models/                    # Model files
│   ├── logs/                      # Log files
│   │   └── atlus.log
│   └── context/                   # Context management
│
├── 📚 DOCUMENTATION
│   ├── README.md                  # Main documentation
│   ├── FLASK_STRUCTURE.md         # Flask structure guide
│   ├── RESTRUCTURE_SUMMARY.md     # Restructuring summary
│   ├── PROJECT_STRUCTURE.md       # This file
│   ├── API_DOCUMENTATION.md       # API reference
│   ├── AGENT_ARCHITECTURE.md      # Agent architecture
│   ├── LOGGING_GUIDE.md           # Logging guide
│   └── AECHITECTURE.md            # Overall architecture
│
└── ⚙️ CONFIGURATION
    ├── requirements.txt           # Python dependencies
    ├── .env                       # Environment variables
    └── .gitignore                 # Git ignore rules
```

## 🔄 Request Flow

```
1. HTTP Request
   └─> Flask App (app/server.py)
       └─> Middleware (app/core/middleware.py)
           └─> Route Handler (app/api/v1/routes/chat.py)
               └─> Validator (app/api/v1/validators.py)
                   └─> Service (app/services/chat_service.py)
                       └─> Orchestrator (orchestrator/orchestrator.py)
                           ├─> Intent Classification
                           │   └─> LLM Router (llm/router.py)
                           │       └─> IntentLLM (llm/intent_llm.py)
                           │           └─> Classifier Prompt (prompts/classifier_prompt.py)
                           │
                           └─> Agent Selection
                               ├─> SimpleAgent (agent/simple_agent.py)
                               │   └─> ChatLLM (llm/chat_llm.py)
                               │       └─> Chat Prompt (prompts/chat_prompt.py)
                               │
                               └─> TaskAgent (agent/task_agent.py)
                                   ├─> Intent Extraction
                                   ├─> Planning
                                   ├─> Reasoning
                                   ├─> Verification
                                   ├─> Refactoring
                                   └─> Final Writing
```

## 📦 Package Responsibilities

### Root Level (Core AI)
| Package | Purpose | Key Files |
|---------|---------|-----------|
| `orchestrator/` | Request routing & intent classification | `orchestrator.py` |
| `agent/` | Agent implementations | `simple_agent.py`, `task_agent.py` |
| `llm/` | LLM interfaces & factory | `router.py`, `*_llm.py` |
| `prompts/` | Prompt builders | `*_prompt.py` |
| `utils/` | Core utilities | `logger.py`, `parsers/`, `validators/` |

### App Level (Flask API)
| Package | Purpose | Key Files |
|---------|---------|-----------|
| `app/api/v1/routes/` | HTTP endpoints | `chat.py`, `health.py` |
| `app/services/` | Business logic | `chat_service.py` |
| `app/core/` | Middleware & extensions | `middleware.py`, `extensions.py` |
| `app/utils/` | Flask utilities | `logger.py` |

## 🎯 Import Patterns

### ✅ Correct Imports

```python
# Root-level packages (orchestrator, agent, llm, prompts, utils)
from orchestrator.orchestrator import Orchestrator
from agent.simple_agent import SimpleAgent
from llm.router import get_llm
from prompts.chat_prompt import build_simple_prompt
from utils.logger import get_logger

# Flask app packages (app.*)
from app.services.chat_service import ChatService
from app.core.middleware import rate_limit
from app.api.v1.schemas import ChatRequestSchema
```

### ❌ Incorrect Imports

```python
# Don't mix patterns
from app.llm.router import get_llm           # ❌ Wrong
from app.orchestrator.orchestrator import Orchestrator  # ❌ Wrong
from services.chat_service import ChatService  # ❌ Wrong
```

## 📊 Statistics

- **Total Python Files**: 56
- **Flask API Files**: 25
- **Core AI Files**: 31
- **Lines of Code**: ~4,500
- **API Endpoints**: 3 (/, /api/v1/chat, /api/v1/health)
- **Agents**: 2 (Simple, Task)
- **LLMs**: 7 (Intent, Planner, Reasoning, Verifier, Writer, Chat, Router)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run API Server
```bash
python run_api.py
```

### 4. Test Endpoint
```bash
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## 🎨 Design Principles

1. **Separation of Concerns**: Core AI logic separate from API
2. **Single Responsibility**: Each file has one clear purpose
3. **Dependency Injection**: Services depend on abstractions
4. **Factory Pattern**: LLM router for instance creation
5. **Blueprint Pattern**: Modular Flask routes
6. **Service Layer**: Business logic separate from HTTP
7. **Middleware Pattern**: Cross-cutting concerns
8. **Configuration Management**: Environment-based settings

## 📖 Documentation

- [Flask Structure](FLASK_STRUCTURE.md) - Detailed Flask guide
- [Restructure Summary](RESTRUCTURE_SUMMARY.md) - What changed
- [Agent Architecture](AGENT_ARCHITECTURE.md) - How agents work
- [API Documentation](API_DOCUMENTATION.md) - API reference
- [Logging Guide](LOGGING_GUIDE.md) - Logging best practices

## 🎯 Key Benefits

✅ **Maintainable**: Clear structure, easy to locate code  
✅ **Scalable**: Add new features without changing existing code  
✅ **Testable**: Each layer can be tested independently  
✅ **Team-Friendly**: Clear boundaries enable parallel work  
✅ **Production-Ready**: Industry-standard patterns  
✅ **Documented**: Comprehensive documentation  

---

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: 2026-01-12

