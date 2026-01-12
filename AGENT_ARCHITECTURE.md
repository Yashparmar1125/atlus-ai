# ATLUS Agent Architecture

## Overview

ATLUS now uses an intelligent routing system that classifies user intent and routes requests to specialized agents, avoiding unnecessary processing for simple requests.

## Architecture Flow

```
User Input
    ↓
Intent Classification (Simple vs Complex)
    ↓
    ├── Simple → SimpleAgent (Single LLM call)
    │            ↓
    │         Quick Response
    │
    └── Complex → TaskAgent (Full Pipeline)
                  ↓
                  Intent Extraction
                  ↓
                  Planning
                  ↓
                  Reasoning
                  ↓
                  Verification
                  ↓
                  Refactoring
                  ↓
                  Final Writing
                  ↓
                  Response
```

## Components

### 1. Agent Orchestrator (`app/agent/agent.py`)

**Purpose**: Main entry point that classifies intent and routes to appropriate agent.

**Responsibilities**:
- Classify user intent (simple vs complex)
- Route to SimpleAgent or TaskAgent
- Handle errors and fallbacks
- Log routing decisions

**Key Methods**:
- `run(user_message)`: Main entry point
- `_classify_intent(user_message)`: Classifies intent using heuristics + LLM
- `_get_simple_agent()`: Lazy-load SimpleAgent
- `_get_task_agent()`: Lazy-load TaskAgent

**Classification Logic**:
1. **Heuristic Check**: Quick keyword-based classification for obvious cases
2. **LLM Classification**: Uses classifier prompt for ambiguous cases
3. **Fallback**: Defaults to complex agent if classification fails

### 2. Simple Agent (`app/agent/simple_agent.py`)

**Purpose**: Handle basic interactions with minimal processing.

**Use Cases**:
- Greetings (hi, hello, hey)
- Simple questions
- Casual conversation
- Thanks/goodbye

**Processing**:
- Single LLM call (WriterLLM)
- No planning, reasoning, or verification
- Fast response times (~2-3 seconds)

**Key Methods**:
- `run(user_message)`: Process simple message
- `_build_simple_prompt(user_message)`: Build conversational prompt

### 3. Task Agent (`app/agent/task_agent.py`)

**Purpose**: Handle complex tasks requiring full pipeline processing.

**Use Cases**:
- Complex task requests
- Implementation requests
- Planning requests
- Problem-solving tasks
- Multi-step workflows

**Processing Pipeline**:
1. **Intent Extraction**: Parse structured intent (goal, constraints, expected output)
2. **Planning**: Generate execution plan (ordered steps)
3. **Reasoning**: Generate comprehensive draft solution
4. **Verification**: Identify issues and suggest fixes
5. **Refactoring**: Improve draft based on verification feedback
6. **Final Writing**: Generate polished final response

**Key Methods**:
- `run(user_message)`: Execute full pipeline
- `_safe_intent_extraction()`: Extract and validate intent
- `_safe_plan_creation()`: Create and validate plan
- `_execute_reasoning()`: Generate comprehensive draft
- `_verify_output()`: Verify and critique draft
- `_refactor_draft()`: Improve draft based on feedback
- `_write_final_response()`: Generate final output

## Classification Details

### Intent Types

| Type | Description | Examples |
|------|-------------|----------|
| **Simple** | Greetings, simple questions, casual conversation | "hi", "hello", "how are you?", "thanks" |
| **Complex** | Tasks requiring planning and implementation | "build a web app", "create a REST API", "solve this problem" |

### Classification Methods

1. **Heuristic Classification** (Fast):
   - Checks for simple keywords (hi, hello, hey, thanks, bye)
   - Checks for complex keywords (build, create, implement, design)
   - Short messages (< 20 chars) with simple keywords → Simple
   - Long messages (> 15 chars) with complex keywords → Complex

2. **LLM Classification** (Accurate):
   - Uses classifier prompt for ambiguous cases
   - Returns: `{"intent_type": "simple"|"complex", "confidence": 0.0-1.0, "reasoning": "..."}`
   - Validated with `ClassifierValidationError`

3. **Fallback**:
   - If classification fails → Default to Complex (safer)
   - If agent fails → Fallback to SimpleAgent

## Benefits

### Performance

- **Simple requests**: ~2-3 seconds (vs ~30-45 seconds with full pipeline)
- **Resource savings**: No unnecessary LLM calls for greetings
- **User experience**: Fast responses for common interactions

### Scalability

- **Lazy loading**: Agents created only when needed
- **Modular design**: Easy to add new agent types
- **Separation of concerns**: Each agent handles specific use cases

### Maintainability

- **Clear separation**: Simple vs complex logic separated
- **Extensible**: Easy to add new specialized agents
- **Testable**: Each agent can be tested independently

## Example Flows

### Simple Request Flow

```
User: "Hi"
  ↓
Agent Orchestrator classifies as "simple"
  ↓
Routes to SimpleAgent
  ↓
Single LLM call (WriterLLM)
  ↓
Response: "Hello! How can I help you today?"
Time: ~2-3 seconds
```

### Complex Request Flow

```
User: "Build a web application with authentication"
  ↓
Agent Orchestrator classifies as "complex"
  ↓
Routes to TaskAgent
  ↓
1. Intent Extraction → {"goal": "Build web app", ...}
  ↓
2. Planning → ["Setup project", "Implement auth", ...]
  ↓
3. Reasoning → Comprehensive draft solution
  ↓
4. Verification → Issues and fixes identified
  ↓
5. Refactoring → Improved draft
  ↓
6. Final Writing → Polished response
  ↓
Response: Full implementation guide
Time: ~30-45 seconds
```

## Adding New Agents

To add a new specialized agent:

1. **Create agent class** in `app/agent/`:
   ```python
   class MySpecialAgent:
       def run(self, user_message: str) -> str:
           # Your logic here
           return response
   ```

2. **Update classifier** to recognize new intent type:
   - Add new type to `classifier_prompt.py`
   - Update `ClassifierValidationError` validator

3. **Update orchestrator** to route to new agent:
   - Add classification logic in `_classify_intent()`
   - Add routing logic in `run()`
   - Add lazy loader method `_get_my_special_agent()`

## Configuration

All agents use the same LLM configuration from `app/llm/config.py` and router from `app/llm/router.py`.

## Logging

All agents log to the same logger system:
- `atlus.agent`: Orchestrator logs
- `atlus.agent.simple`: SimpleAgent logs
- `atlus.agent.task`: TaskAgent logs

Logs include:
- Classification decisions
- Routing information
- Execution times
- Errors and fallbacks



