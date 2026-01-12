# Prompts & Rules Refactoring Summary

## What Was Done

### 1. ✅ Created Rules Folder Structure
- **New folder**: `rules/` containing all editable rules
- **8 rule files** organized by functionality
- **Clean separation** between rules and prompt logic

### 2. ✅ Extracted Rules from Prompts

#### Rules Extracted:
- **Behavior Rules** → `rules/behavior_rules.py`
  - Brand & identity rules
  - Behavior rules
  - Interaction guidelines
  - Restrictions
  - **NEW**: Memory usage instructions

- **JSON Schemas** → `rules/json_schemas.py`
  - Intent schema
  - Plan schema
  - Classifier schema
  - Verifier schema
  - JSON output instruction

- **Classification Rules** → `rules/classification_rules.py`
  - Classification criteria
  - Simple/complex examples

- **Plan Constraints** → `rules/plan_constraints.py`
  - Plan structure rules
  - Plan examples

- **Verifier Rules** → `rules/verifier_rules.py`
  - Verification rules
  - Verification examples

- **Reasoning Rules** → `rules/reasoning_rules.py`
  - Reasoning instructions
  - **NEW**: Memory context instructions

- **Refactor Rules** → `rules/refactor_rules.py`
  - Refactoring guidelines

- **Writer Rules** → `rules/writer_rules.py`
  - Final writing guidelines

### 3. ✅ Updated All Prompts

All prompts now import and use rules:

| Prompt File | Rules Used |
|------------|-----------|
| `prompts/chat_prompt.py` | `behavior_rules.py` |
| `prompts/classifier_prompt.py` | `classification_rules.py` + `json_schemas.py` |
| `prompts/intent_prompt.py` | `json_schemas.py` |
| `prompts/planner_prompt.py` | `plan_constraints.py` + `json_schemas.py` |
| `prompts/reasoning_prompt.py` | `reasoning_rules.py` |
| `prompts/verifier_prompt.py` | `verifier_rules.py` + `json_schemas.py` |
| `prompts/refactor_prompt.py` | `refactor_rules.py` |
| `prompts/writer_prompt.py` | `writer_rules.py` |

### 4. ✅ Added Memory-Aware Instructions

**New memory instructions added:**
- `behavior_rules.get_memory_usage_instructions()` - How to use memory in conversations
- `reasoning_rules.get_memory_context_instruction()` - How to use memory in reasoning

**Integration:**
- Memory instructions are automatically included in prompts
- Agents now aware of memory context usage
- Maintains consistency with memory architecture

## Benefits

### Before
```python
# Hardcoded rules in prompts
def build_simple_prompt(user_message: str):
    return [{
        "role": "system",
        "content": (
            "Brand & identity rules:\n"
            "- Always acknowledge yourself as ATLUS...\n"  # Hardcoded!
            # Rules scattered, hard to update
        )
    }]
```

### After
```python
# Rules separated, prompts use rules
from rules.behavior_rules import get_brand_identity_rules

def build_simple_prompt(user_message: str):
    return [{
        "role": "system",
        "content": f"Brand & identity rules:\n{get_brand_identity_rules()}\n\n..."
    }]
```

### Advantages:
1. ✅ **Single Source of Truth** - Rules live in one place
2. ✅ **Easy Updates** - Change rules without touching prompt code
3. ✅ **Maintainability** - Clear separation of concerns
4. ✅ **Testability** - Rules can be tested independently
5. ✅ **Consistency** - All prompts use same rule definitions
6. ✅ **Memory Integration** - Rules include memory-aware instructions

## File Structure

```
ATLUS/
├── rules/                          # NEW: Rules folder
│   ├── __init__.py
│   ├── behavior_rules.py
│   ├── json_schemas.py
│   ├── classification_rules.py
│   ├── plan_constraints.py
│   ├── verifier_rules.py
│   ├── reasoning_rules.py
│   ├── refactor_rules.py
│   └── writer_rules.py
│
├── prompts/                        # UPDATED: Now uses rules
│   ├── __init__.py
│   ├── chat_prompt.py              # ✅ Uses behavior_rules
│   ├── classifier_prompt.py        # ✅ Uses classification_rules + json_schemas
│   ├── intent_prompt.py            # ✅ Uses json_schemas
│   ├── planner_prompt.py           # ✅ Uses plan_constraints + json_schemas
│   ├── reasoning_prompt.py         # ✅ Uses reasoning_rules
│   ├── verifier_prompt.py          # ✅ Uses verifier_rules + json_schemas
│   ├── refactor_prompt.py          # ✅ Uses refactor_rules
│   └── writer_prompt.py            # ✅ Uses writer_rules
│
└── memory/                         # EXISTING: Memory system
    └── ...
```

## Usage Examples

### Updating Behavior Rules
```python
# Edit rules/behavior_rules.py
def get_brand_identity_rules() -> str:
    return (
        "- Always acknowledge yourself as ATLUS in greetings.\n"
        "- NEW: Be more casual in informal contexts.\n"  # Just add here!
    )
# All prompts automatically use updated rules!
```

### Testing Rules
```python
# tests/test_rules.py
from rules.behavior_rules import get_brand_identity_rules

def test_brand_rules():
    rules = get_brand_identity_rules()
    assert "ATLUS" in rules
```

### Using Rules in Prompts
```python
# prompts/chat_prompt.py
from rules.behavior_rules import get_brand_identity_rules

def build_simple_prompt(user_message: str):
    return [{
        "role": "system",
        "content": f"Brand rules:\n{get_brand_identity_rules()}"
    }]
```

## Memory Integration Status

✅ **Memory-aware instructions added:**
- Behavior rules include memory usage guidelines
- Reasoning rules include memory context instructions
- Prompts automatically include memory instructions
- Compatible with memory system architecture

## Testing

✅ **Verification:**
- All rules import correctly
- All prompts updated successfully
- No linter errors
- Rules are functional and testable

## Next Steps (Optional)

1. **Rule Validation**: Add validators for rule format
2. **Rule Versioning**: Track rule changes
3. **Rule A/B Testing**: Easy rule set swapping
4. **Rule Documentation**: Auto-generate docs
5. **Rule Templates**: Parameterized rules

---

**Status**: ✅ **Complete**
- Rules separated from prompts
- All prompts refactored
- Memory integration complete
- No breaking changes
- Backward compatible

