# Memory Integration Guide

## Overview

ATLUS now includes a sophisticated memory system that maintains conversation context, user preferences, and task state across sessions.

## Memory Architecture

### 4 Types of Memory

```
┌─────────────────────────────────────────────────────────┐
│                    ATLUS Memory System                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Session Memory    → Recent conversation turns        │
│  2. Working Memory    → Current task decisions           │
│  3. Long-Term Memory  → Persistent user facts            │
│  4. Behavior Profile  → Interaction style settings       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 1. Session Memory
- **Purpose**: Maintain conversation continuity
- **Storage**: In-memory (last 6 turns)
- **Scope**: Per session
- **Lifetime**: Until session ends

```python
from memory import SessionMemory

session = SessionMemory("session_123")
session.add_turn("Hello", "Hi! How can I help you?")
context = session.get_context()  # Returns message list
```

### 2. Working Memory
- **Purpose**: Track task-level decisions and constraints
- **Storage**: In-memory dictionary
- **Scope**: Per session
- **Lifetime**: Until session ends

```python
from memory import WorkingMemory

working = WorkingMemory("session_123")
working.update("tech_stack", ["Python", "Flask"])
working.update("constraint", "no paid APIs")
facts = working.get_all()
```

### 3. Long-Term Memory
- **Purpose**: Persistent user preferences and facts
- **Storage**: JSON files in `data/` directory
- **Scope**: Per user
- **Lifetime**: Persistent across sessions

```python
from memory import LongTermMemory

long_term = LongTermMemory("user_123")
long_term.update("preferred_language", "Python")
long_term.update("prefers_free_tier", True)
prefs = long_term.get_all()
```

### 4. Behavior Profile
- **Purpose**: Control interaction style
- **Storage**: In-memory profile
- **Scope**: Per session
- **Lifetime**: Adapts during conversation

```python
from memory import BehaviorProfile, Verbosity, Tone, Depth

behavior = BehaviorProfile()
behavior.set_verbosity(Verbosity.HIGH)
behavior.set_tone(Tone.TECHNICAL)
behavior.adapt_from_user_message("explain in detail how this works")
```

## Integration Points

### 1. Orchestrator
Receives pre-built context with memory:

```python
# orchestrator/orchestrator.py
def run(self, user_message: str, session_id: str = "default", context_messages: list = None):
    # Uses context_messages if provided
    response = agent.run(user_message, context_messages=context_messages)
```

### 2. Agents
Both SimpleAgent and TaskAgent accept context:

```python
# agent/simple_agent.py
def run(self, user_message: str, context_messages: list = None):
    if context_messages:
        # Use context with memory
        prompt = context_messages
        prompt.append({"role": "user", "content": user_message})
    else:
        # Fallback to simple prompt
        prompt = build_simple_prompt(user_message)
```

### 3. ChatService
Manages memory lifecycle:

```python
# app/services/chat_service.py
def process_chat(cls, payload, request_id):
    # 1. Build context with memory
    context_messages = MemoryService.build_context(
        system_prompt=system_prompt,
        session_id=session_id,
        user_id=user_id,
        user_message=message
    )
    
    # 2. Run orchestrator
    response = orchestrator.run(message, session_id, context_messages)
    
    # 3. Save turn to memory
    MemoryService.save_turn(session_id, message, response)
```

### 4. MemoryService
Centralized memory management:

```python
# app/services/memory_service.py
class MemoryService:
    @classmethod
    def build_context(cls, system_prompt, session_id, user_id, user_message):
        # Assembles context from all memory types
        
    @classmethod
    def save_turn(cls, session_id, user_message, agent_response):
        # Saves conversation turn
        
    @classmethod
    def clear_session(cls, session_id):
        # Clears session data
```

## Request Flow with Memory

```
1. User sends message
   ↓
2. ChatService receives request
   ↓
3. MemoryService.build_context()
   ├─> Load SessionMemory (recent turns)
   ├─> Load WorkingMemory (task decisions)
   ├─> Load LongTermMemory (user preferences)
   ├─> Load BehaviorProfile (interaction style)
   └─> ContextAssembler.build_context()
       └─> Returns message list with all memory
   ↓
4. Orchestrator.run(message, session_id, context_messages)
   ├─> Classify intent
   └─> Route to agent
       └─> Agent uses context_messages (includes memory)
   ↓
5. Agent generates response
   ↓
6. MemoryService.save_turn()
   └─> Save to SessionMemory
   ↓
7. Return response
```

## Context Assembly

The `ContextAssembler` builds prompts with memory:

```python
messages = [
    # 1. System prompt + Behavior profile
    {
        "role": "system",
        "content": "You are ATLUS...\n\nInteraction style:\n- Verbosity: medium\n- Tone: neutral\n- Depth: normal"
    },
    
    # 2. Long-term memory (if any)
    {
        "role": "system",
        "content": "User Context & Preferences:\n- preferred_language: Python\n- prefers_free_tier: True"
    },
    
    # 3. Working memory (if any)
    {
        "role": "system",
        "content": "Current Task State:\n{'tech_stack': ['Flask', 'React']}"
    },
    
    # 4. Session history (last 6 turns)
    {"role": "user", "content": "Previous message 1"},
    {"role": "assistant", "content": "Previous response 1"},
    {"role": "user", "content": "Previous message 2"},
    {"role": "assistant", "content": "Previous response 2"},
    
    # 5. Current message (added by agent)
    {"role": "user", "content": "Current message"}
]
```

## API Usage

### Chat Request with Session
```bash
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "session_id": "user_session_123",
    "user_id": "user_123"
  }'
```

### Continuing Conversation
```bash
# Second message in same session
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What did I just say?",
    "session_id": "user_session_123",
    "user_id": "user_123"
  }'
```

**Note**: The agent will remember the previous message because it's stored in `SessionMemory`.

## Memory Behavior

### Session Memory
- Keeps last **6 turns** (configurable)
- Automatically truncates old history
- Provides conversation continuity

### Working Memory
- Stores task-level decisions
- Examples:
  - Technology choices
  - Constraints
  - Current task state
- Cleared when session ends

### Long-Term Memory
- Persisted to disk: `data/memory_{user_id}.json`
- Stores user preferences
- Shared across all sessions for a user
- Examples:
  - Preferred language
  - API key preferences
  - Common patterns

### Behavior Profile
- Adapts automatically based on user messages
- Controls:
  - **Verbosity**: low, medium, high
  - **Tone**: casual, neutral, technical
  - **Depth**: shallow, normal, advanced
- Injected into system prompt

### Auto-Adaptation Examples

| User Message | Behavior Change |
|-------------|-----------------|
| "hi" (3 words or less) | Verbosity → LOW |
| "explain in detail how this works" | Depth → ADVANCED, Verbosity → HIGH |
| "hey yo sup" | Tone → CASUAL |
| "discuss the architecture and scalability" | Tone → TECHNICAL |

## Memory Lifecycle

### Session Start
```python
# Automatically created on first message
session = MemoryService.get_session_memory("session_123")
working = MemoryService.get_working_memory("session_123")
behavior = MemoryService.get_behavior_profile("session_123")
long_term = MemoryService.get_long_term_memory("user_123")
```

### During Conversation
```python
# After each turn
MemoryService.save_turn(session_id, user_message, agent_response)
```

### Session End
```python
# Clear session data
MemoryService.clear_session("session_123")
```

### Persistence
- **Session Memory**: Not persisted (in-memory only)
- **Working Memory**: Not persisted (in-memory only)
- **Long-Term Memory**: Auto-saved to JSON on update
- **Behavior Profile**: Not persisted (resets each session)

## Production Considerations

### Current (Development)
- Session/Working memory: In-memory Python dictionaries
- Long-term memory: JSON files
- Single-server only

### Recommended (Production)
- Session/Working memory: Redis with TTL
- Long-term memory: PostgreSQL or MongoDB
- Behavior profiles: Redis with session TTL
- Distributed: Share state across servers

## Testing Memory

```python
# Test script
from app.services.memory_service import MemoryService

# Create session
session_id = "test_session"

# First message
context1 = MemoryService.build_context(
    system_prompt="You are ATLUS",
    session_id=session_id,
    user_message="My name is John"
)
# Use context1 with agent...

# Save turn
MemoryService.save_turn(session_id, "My name is John", "Nice to meet you, John!")

# Second message
context2 = MemoryService.build_context(
    system_prompt="You are ATLUS",
    session_id=session_id,
    user_message="What's my name?"
)
# context2 now includes the previous turn
# Agent should respond: "Your name is John"

# Check stats
stats = MemoryService.get_session_stats(session_id)
print(stats)  # Shows conversation_turns, memory status
```

## Files Modified

1. ✅ `memory/__init__.py` - Package exports
2. ✅ `memory/*.py` - Added docstrings
3. ✅ `app/services/memory_service.py` - Memory management service
4. ✅ `orchestrator/orchestrator.py` - Accept context_messages
5. ✅ `agent/simple_agent.py` - Use context_messages
6. ✅ `agent/task_agent.py` - Use context_messages
7. ✅ `app/services/chat_service.py` - Build and save memory
8. ✅ `app/api/v1/schemas.py` - Add user_id field
9. ✅ `run.py` - Example with memory

## Benefits

✅ **Continuity**: Remembers conversation history  
✅ **Consistency**: Maintains task decisions  
✅ **Personalization**: Adapts to user preferences  
✅ **Intelligence**: Feels more coherent and aware  
✅ **Scalability**: Easy to swap storage backend  
✅ **Clean**: Memory logic separate from AI logic  

---

**Status**: ✅ Fully Integrated  
**Files**: Memory system integrated across all layers  
**Testing**: Ready for testing with session management


