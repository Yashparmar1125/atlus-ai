

# 🧠 First: the governing rule (non-negotiable)

> **Memory is not chat history.
> Memory is structured state used to build context.**

So memory lives **outside** the model and is **selectively injected**.

---

# 🧩 The 4 Memory Types — IMPLEMENTATION LEVEL

We’ll implement each as a **separate module**, with **clear read/write rules**.

```
memory/
├── session_memory.py
├── working_memory.py
├── long_term_memory.py
├── behavior_profile.py
└── context_assembler.py
```

---

## 1️⃣ Session Memory (short-term conversation)

### Purpose

* Maintain conversational continuity
* Avoid repetition
* Support follow-ups

### What is stored

* Last N turns
* Summaries, not raw logs

---

### 📁 `memory/session_memory.py`

```python
class SessionMemory:
    def __init__(self, max_turns=6):
        self.turns = []
        self.max_turns = max_turns

    def add(self, role: str, content: str):
        self.turns.append({"role": role, "content": content})
        self.turns = self.turns[-self.max_turns:]

    def get(self):
        return self.turns

    def clear(self):
        self.turns = []
```

### Usage

```python
session.add("user", user_message)
session.add("assistant", response)
```

⚠️ **Never** send this whole thing blindly to the model.

---

## 2️⃣ Working Memory (task-level intelligence)

This is the **most important memory**.

### Purpose

* Preserve decisions
* Maintain constraints
* Ensure consistency across turns

### Stored as **structured facts**

---

### 📁 `memory/working_memory.py`

```python
class WorkingMemory:
    def __init__(self):
        self.data = {}

    def set(self, key: str, value):
        self.data[key] = value

    def get(self, key: str):
        return self.data.get(key)

    def snapshot(self):
        return self.data.copy()

    def clear(self):
        self.data = {}
```

### Example writes

```python
working.set("tech_stack", ["FastAPI", "React"])
working.set("constraint", "no paid APIs")
working.set("auth_method", "JWT")
```

### Example reads

```python
if working.get("constraint") == "no paid APIs":
    suggest_open_source()
```

This is how **multi-turn coherence** happens.

---

## 3️⃣ Long-Term Memory (persistent, cross-session)

### Purpose

* User preferences
* Stable facts
* Reusable knowledge

### Storage

* JSON (initial)
* DB / vector store (later)

---

### 📁 `memory/long_term_memory.py`

```python
import json
from pathlib import Path

class LongTermMemory:
    FILE = Path("memory_store.json")

    def load(self):
        if self.FILE.exists():
            return json.loads(self.FILE.read_text())
        return {}

    def save(self, data: dict):
        self.FILE.write_text(json.dumps(data, indent=2))

    def update(self, key, value):
        data = self.load()
        data[key] = value
        self.save(data)

    def get(self, key):
        return self.load().get(key)
```

### Example

```python
long_term.update("preferred_language", "Python")
long_term.update("prefers_free_tier", True)
```

⚠️ This memory must be:

* sparse
* explicit
* user-safe

---

## 4️⃣ Behavior Profile (interaction style)

This controls **how** ATLUS talks, not **what** it says.

### Purpose

* Adjust verbosity
* Adjust tone
* Adapt depth

---

### 📁 `memory/behavior_profile.py`

```python
class BehaviorProfile:
    def __init__(self):
        self.profile = {
            "verbosity": "medium",
            "tone": "neutral",
            "depth": "normal"
        }

    def update(self, key, value):
        self.profile[key] = value

    def snapshot(self):
        return self.profile.copy()
```

### Example

```python
behavior.update("depth", "advanced")
behavior.update("verbosity", "high")
```

---

# 🧠 The MOST IMPORTANT PART

## How memory is USED → Context Assembly

This is where intelligence actually happens.

---

## 📁 `memory/context_assembler.py`

```python
def build_context(
    system_prompt: str,
    session_memory,
    working_memory,
    behavior_profile
):
    context = []

    context.append({
        "role": "system",
        "content": system_prompt
    })

    if behavior_profile:
        context.append({
            "role": "system",
            "content": f"Interaction style: {behavior_profile}"
        })

    if working_memory:
        context.append({
            "role": "system",
            "content": f"Working memory:\n{working_memory}"
        })

    if session_memory:
        context.extend(session_memory)

    return context
```

### Key rule

❌ Don’t inject everything
✅ Inject **only what matters for this step**

---

# 🔁 Full Memory Lifecycle (End-to-End)

```
User Message
   ↓
Intent Classification
   ↓
Session Memory ← store user message
   ↓
Working Memory ← update decisions
   ↓
Context Assembler
   ↓
Agent / LLM Call
   ↓
Post-Execution Filter
   ↓
Session Memory ← store response
   ↓
Long-Term Memory ← store preferences (optional)
```

---

# 🔍 What gets written vs ignored

| Data                | Stored? | Why         |
| ------------------- | ------- | ----------- |
| Greeting            | ❌       | noise       |
| User constraints    | ✅       | critical    |
| Tech decisions      | ✅       | consistency |
| Intermediate drafts | ❌       | too verbose |
| Final decisions     | ✅       | reusable    |
| Verifier output     | ❌       | internal    |

Memory is **curated**, not logged.

---

# 🧠 Why multi-model systems still feel coherent

Because:

* Memory is **shared**
* Context is **assembled centrally**
* Models are **stateless workers**

The user never talks to:

> GPT / LLaMA / Qwen

They talk to:

> **ATLUS (the system)**

---

# 🏁 Final mental model (lock this in)

> **Memory is a database.
> Context is a query.
> The model is a function.**

Once you internalize this:

* small models feel smart
* conversations feel continuous
* agent systems scale cleanly

---

