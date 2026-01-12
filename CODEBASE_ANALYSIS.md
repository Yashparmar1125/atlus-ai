# ATLUS Codebase Analysis

## 📋 Executive Summary

**ATLUS** is an agentic AI assistant system that uses a multi-stage LLM pipeline to process user requests. The architecture follows a structured workflow: **Intent Extraction → Planning → Reasoning → Verification → Final Writing**.

### Current Status
- ✅ Core architecture implemented
- ✅ Multi-LLM pipeline structure in place
- ❌ **Critical bug** preventing execution
- ❌ Missing dependencies in requirements.txt
- ⚠️ Import path inconsistencies

---

## 🏗️ Architecture Overview

### System Flow
```
User Input → Intent Extraction → Planning → Stepwise Reasoning → Verification → Final Writing → Response
```

### Component Breakdown

#### 1. **Agent (`app/agent/agent.py`)**
- **Purpose**: Main orchestrator controlling the entire pipeline
- **Key Methods**:
  - `run()`: Public entry point
  - `_safe_intent_extraction()`: Extracts user intent with retry logic
  - `_safe_plan_creation()`: Creates execution plan with validation
  - `_execute_plan_stepwise()`: Executes plan step-by-step
  - `_verify_output()`: Critiques the draft output
  - `_write_final_response()`: Produces polished final response
  - `_repair()`: Error recovery mechanism

#### 2. **LLM Layer (`app/llm/`)**
Five specialized LLM classes, all inheriting from `BaseLLM`:

| LLM Class | Purpose | Model Config | Reasoning Enabled |
|-----------|---------|--------------|-------------------|
| `IntentLLM` | Extract structured intent | nemotron-3-nano-30b | ❌ False |
| `PlanningLLM` | Generate execution plan | gpt-oss-20b | ✅ True |
| `ReasoningLLM` | Step-by-step reasoning | trinity-mini | ✅ True |
| `VerifierLLM` | Critique and validate | nemotron-3-nano-30b | ✅ True |
| `WriterLLM` | Final polished output | nemotron-3-nano-30b | ❌ False |

**Provider**: All use OpenRouter API with free tier models

#### 3. **Prompts (`app/prompts/`)**
Specialized prompt builders for each stage:
- `intent_prompt.py`: Extracts goal, constraints, expected_output
- `planner_prompt.py`: Generates ordered step list
- `reasoning_prompt.py`: Step-by-step execution
- `verifier_prompt.py`: Error detection and feedback
- `writer_prompt.py`: Clean, user-facing output

#### 4. **Utilities (`app/utils/`)**
- **Parsers**: JSON and plan parsing with error handling
- **Validators**: Intent and plan validation with type checking

---

## 🐛 Critical Issues

### 1. **BUG: KeyError in `intent_llm.py` (Line 25)**
**Location**: `app/llm/intent_llm.py:25`

**Problem**:
```python
extra_body={
    "reasoning": {"enabled": self.cfg["intent"]}  # ❌ KeyError: 'intent'
}
```

**Root Cause**: `self.cfg` is already `MODELS["intent"]`, so accessing `self.cfg["intent"]` tries to find a nested key that doesn't exist.

**Fix**: Should be:
```python
extra_body={
    "reasoning": {"enabled": False}  # or self.cfg.get("reasoning", False)
}
```

**Impact**: ⚠️ **BLOCKS ALL EXECUTION** - This is why `test.py` fails.

---

### 2. **Import Error in `router.py`**
**Location**: `app/llm/router.py:4`

**Problem**:
```python
from llm.planner_llm import PlannerLLM  # ❌ Wrong class name
```

**Root Cause**: The actual file is `planning_llm.py` with class `PlanningLLM`.

**Fix**: Should be:
```python
from llm.planning_llm import PlanningLLM
```

**Impact**: ⚠️ **Medium** - Router is not currently used, but will break if used.

---

### 3. **Missing Dependencies**
**Location**: `requirements.txt` is empty

**Required Packages** (based on code analysis):
- `openai` - OpenAI SDK for API calls
- `python-dotenv` - Environment variable management
- `requests` - (used in `run.py`)

**Impact**: ⚠️ **High** - Project cannot be set up without manual installation.

---

### 4. **Import Path Structure**
**Issue**: All imports use relative paths (e.g., `from llm.intent_llm`), which means:
- Code must be run from `app/` directory, OR
- `app/` must be in PYTHONPATH, OR
- Imports should be absolute (`from app.llm.intent_llm`)

**Current Pattern**:
```python
# In agent.py
from llm.intent_llm import IntentLLM  # Relative import
```

**Impact**: ⚠️ **Medium** - May cause import errors depending on execution context.

---

## 📊 Code Quality Assessment

### ✅ Strengths
1. **Clear Separation of Concerns**: Each LLM has a single responsibility
2. **Error Handling**: Retry logic and repair mechanisms in place
3. **Validation**: Input validation at each stage
4. **Structured Outputs**: JSON parsing and validation ensure reliability
5. **Modular Design**: Easy to swap models or add new stages

### ⚠️ Areas for Improvement
1. **Error Recovery**: `_repair()` uses verifier LLM, but no fallback if repair fails
2. **Configuration**: Hard-coded model names in config, no environment-based switching
3. **Logging**: No logging infrastructure visible
4. **Testing**: Only basic test file, no unit tests
5. **Documentation**: Missing docstrings in several classes
6. **Type Hints**: Inconsistent use of type hints

---

## 🔍 Detailed File Analysis

### Core Files

#### `app/agent/agent.py` (169 lines)
- **Status**: ✅ Well-structured
- **Issues**: None critical
- **Dependencies**: All 5 LLMs, all prompt builders, all parsers/validators

#### `app/llm/config.py` (44 lines)
- **Status**: ✅ Good structure
- **Models**: 5 model configurations
- **Note**: Uses `reasoning` key inconsistently (some models have it, some don't)

#### `app/llm/intent_llm.py` (29 lines)
- **Status**: ❌ **BUG PRESENT**
- **Issue**: Line 25 KeyError

#### `app/llm/router.py` (21 lines)
- **Status**: ⚠️ Import error
- **Usage**: Not currently used by agent.py
- **Purpose**: Factory pattern for LLM creation

### Utility Files

#### Parsers (`app/utils/parsers/`)
- `json_parser.py`: Handles markdown-wrapped JSON ✅
- `plan_parser.py`: Flexible plan parsing (strings or objects) ✅

#### Validators (`app/utils/validators/`)
- `intent_validator.py`: Type checking for intent structure ✅
- `plan_validator.py`: Plan validation with length checks ✅

---

## 🚀 Recommendations

### Immediate Fixes (Priority 1)
1. **Fix `intent_llm.py` line 25** - Change `self.cfg["intent"]` to `False`
2. **Add `requirements.txt`** with all dependencies
3. **Fix `router.py` import** - Change `PlannerLLM` to `PlanningLLM`

### Short-term Improvements (Priority 2)
1. **Add logging** - Use Python's `logging` module throughout
2. **Environment variables** - Move API keys and model configs to `.env`
3. **Error handling** - Add more graceful degradation
4. **Type hints** - Complete type annotations

### Long-term Enhancements (Priority 3)
1. **Unit tests** - Add pytest tests for each component
2. **Integration tests** - Test full pipeline
3. **Configuration management** - Use config files or environment
4. **Monitoring** - Add metrics and performance tracking
5. **Caching** - Cache LLM responses for repeated queries

---

## 📁 Project Structure Assessment

### Current Structure
```
app/
├── agent/          ✅ Core logic
├── llm/            ✅ Model abstractions
├── prompts/        ✅ Prompt management
├── utils/          ✅ Parsers & validators
├── api/            ⚠️ Empty (planned)
├── context/        ⚠️ Empty (planned)
├── memory/         ⚠️ Empty (planned)
├── orchestrator/   ⚠️ Empty (planned)
└── tools/          ⚠️ Empty (planned)
```

### Architecture Document vs. Implementation
The `AECHITECTURE.md` describes a more complete system with:
- Context management (conversation history)
- Memory (short-term/long-term)
- Tools (Python exec, RAG)
- Orchestrator layer

**Current State**: Only the core agent pipeline is implemented. The system is functional but lacks the advanced features described in the architecture.

---

## 🧪 Testing Status

### Current Test
- `app/test.py`: Basic integration test
- **Status**: ❌ Fails due to KeyError bug

### Missing Tests
- Unit tests for parsers
- Unit tests for validators
- Unit tests for LLM classes
- Integration tests for full pipeline
- Error handling tests

---

## 🔐 Security Considerations

1. **API Keys**: Currently loaded from `.env` ✅
2. **No hardcoded secrets**: ✅
3. **Input validation**: ✅ Present at multiple stages
4. **Error messages**: ⚠️ May leak internal structure in error responses

---

## 📈 Performance Considerations

1. **Sequential Execution**: Plan steps executed one-by-one (could be parallelized)
2. **No Caching**: Every request hits LLM APIs
3. **Token Limits**: Configured per model (512-2048 tokens)
4. **Retry Logic**: MAX_RETRIES = 2 (reasonable)

---

## 🎯 Conclusion

The codebase demonstrates a **well-architected agentic AI system** with clear separation of concerns and a robust pipeline. However, there are **critical bugs** that prevent execution and **missing infrastructure** (dependencies, tests, logging).

**Overall Assessment**: 🟡 **Good foundation, needs bug fixes and polish**

**Next Steps**:
1. Fix the KeyError bug
2. Add requirements.txt
3. Test the full pipeline
4. Add missing infrastructure (logging, tests)



