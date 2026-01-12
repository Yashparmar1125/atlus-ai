# Intent Classification Fix

## Problem
Simple conversations were being routed to TaskAgent instead of SimpleAgent. The classification was not aggressive enough in favoring simple responses.

## Solution

### 1. Updated Classification Rules
- **Default to 'simple'** unless clearly a heavy task
- Made rules more explicit: simple is DEFAULT
- Added more simple examples (drafting, explanations, questions)
- Restricted complex examples to ONLY heavy implementation tasks

### 2. Updated Orchestrator Logic
- Changed default from `"complex"` to `"simple"` when classification is unclear
- Added confidence threshold: Only use complex if confidence >= 0.8
- Updated heuristic keywords to be more restrictive (only heavy implementation)

### 3. Updated Classification Prompt
- Added explicit instruction to default to 'simple'
- Clarified that drafts, explanations, questions should be simple

## Changes Made

### rules/classification_rules.py
- Rules now explicitly state "DEFAULT to 'simple'"
- Added more simple examples (drafting messages, explanations)
- Complex examples restricted to heavy implementation only

### orchestrator/orchestrator.py
- Default changed from `"complex"` to `"simple"`
- Added confidence threshold (0.8) for complex classification
- Updated heuristic keywords to exclude simple tasks like "write a message"

### prompts/classifier_prompt.py
- Added explicit instruction to default to simple
- Clarified that drafts/explanations/questions are simple

## Result

- Simple conversations → SimpleAgent ✅
- Heavy implementation tasks → TaskAgent ✅
- Better resource usage (TaskAgent only for heavy tasks)
- Faster responses for simple queries

## Data Folder Note

The `data/` folder will only contain files when long-term memory is actually updated. Sessions create in-memory data (session memory, working memory), but long-term memory files are only created when `LongTermMemory.update()` is called.

To test long-term memory:
```python
from memory import LongTermMemory
lt = LongTermMemory("user_123")
lt.update("preference", "value")  # This creates data/memory_user_123.json
```

---

**Status**: ✅ Fixed - Classification now aggressively favors SimpleAgent

