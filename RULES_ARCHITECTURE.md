# Rules Architecture

## Overview

Rules are **separated from prompts** for easier maintenance, updates, and testing. This follows the principle of **separation of concerns**.

## Structure

```
rules/
├── __init__.py              # Package exports
├── behavior_rules.py        # ATLUS personality & interaction rules
├── json_schemas.py          # JSON output schemas
├── classification_rules.py  # Intent classification rules
├── plan_constraints.py      # Plan generation constraints
├── verifier_rules.py        # Verification rules
├── reasoning_rules.py       # Reasoning instructions
├── refactor_rules.py        # Refactoring rules
└── writer_rules.py          # Final writing rules
```

## Design Principles

### 1. **Separation of Concerns**
- **Rules**: Editable configurations and constraints
- **Prompts**: Logic for assembling messages
- **Agents**: Orchestration and execution

### 2. **Single Source of Truth**
- Rules live in one place
- Prompts reference rules (don't duplicate them)
- Changes to rules automatically reflect in all prompts

### 3. **Maintainability**
- Update behavior by editing rules files
- No need to touch prompt code
- Easy to A/B test different rule sets

### 4. **Testability**
- Rules can be unit tested independently
- Prompts can be tested with mock rules
- Easy to validate rule changes

## Rule Categories

### 1. Behavior Rules (`rules/behavior_rules.py`)
Controls ATLUS personality and interaction style.

**Functions:**
- `get_brand_identity_rules()` - Brand & identity guidelines
- `get_behavior_rules()` - General behavior rules
- `get_interaction_guidelines()` - Interaction type guidelines
- `get_restrictions()` - Things to avoid
- `get_memory_usage_instructions()` - How to use memory context

**Usage:**
```python
from rules.behavior_rules import get_brand_identity_rules

rules = get_brand_identity_rules()
# Use in chat_prompt.py
```

### 2. JSON Schemas (`rules/json_schemas.py`)
Defines required JSON structures for structured outputs.

**Functions:**
- `get_intent_schema()` - Intent extraction schema
- `get_plan_schema()` - Plan generation schema
- `get_classifier_schema()` - Classification schema
- `get_verifier_schema()` - Verification schema
- `get_json_output_instruction()` - Standard JSON output instruction

**Usage:**
```python
from rules.json_schemas import get_intent_schema, get_json_output_instruction

schema = get_intent_schema()
instruction = get_json_output_instruction()
# Use in intent_prompt.py
```

### 3. Classification Rules (`rules/classification_rules.py`)
Rules for intent classification (simple vs complex).

**Functions:**
- `get_classification_rules()` - Classification criteria
- `get_simple_examples()` - Examples of simple requests
- `get_complex_examples()` - Examples of complex requests

**Usage:**
```python
from rules.classification_rules import get_classification_rules

rules = get_classification_rules()
# Use in classifier_prompt.py
```

### 4. Plan Constraints (`rules/plan_constraints.py`)
Constraints for plan generation.

**Functions:**
- `get_plan_constraints()` - Plan structure rules
- `get_plan_example()` - Example plan output

**Usage:**
```python
from rules.plan_constraints import get_plan_constraints

constraints = get_plan_constraints()
# Use in planner_prompt.py
```

### 5. Verifier Rules (`rules/verifier_rules.py`)
Rules for verification stage.

**Functions:**
- `get_verifier_rules()` - Verification output rules
- `get_verifier_examples()` - Example verification outputs

**Usage:**
```python
from rules.verifier_rules import get_verifier_rules

rules = get_verifier_rules()
# Use in verifier_prompt.py
```

### 6. Reasoning Rules (`rules/reasoning_rules.py`)
Instructions for reasoning stage.

**Functions:**
- `get_reasoning_instructions()` - Step-by-step execution instructions
- `get_memory_context_instruction()` - How to use memory in reasoning

**Usage:**
```python
from rules.reasoning_rules import get_reasoning_instructions

instructions = get_reasoning_instructions()
# Use in reasoning_prompt.py
```

### 7. Refactor Rules (`rules/refactor_rules.py`)
Rules for refactoring stage.

**Functions:**
- `get_refactor_rules()` - Refactoring guidelines

**Usage:**
```python
from rules.refactor_rules import get_refactor_rules

rules = get_refactor_rules()
# Use in refactor_prompt.py
```

### 8. Writer Rules (`rules/writer_rules.py`)
Rules for final writing stage.

**Functions:**
- `get_writer_rules()` - Final output guidelines

**Usage:**
```python
from rules.writer_rules import get_writer_rules

rules = get_writer_rules()
# Use in writer_prompt.py
```

## Integration with Memory

Rules now include **memory-aware instructions**:

1. **`behavior_rules.get_memory_usage_instructions()`**
   - How to use memory context in conversations
   - When to reference previous conversations
   - How to maintain consistency

2. **`reasoning_rules.get_memory_context_instruction()`**
   - How to use memory in reasoning stage
   - Reference previous decisions
   - Continue from existing task state

## Benefits

### Before (Hardcoded Rules)
```python
# prompts/chat_prompt.py
def build_simple_prompt(user_message: str):
    return [{
        "role": "system",
        "content": (
            "Brand & identity rules:\n"
            "- Always acknowledge yourself as ATLUS...\n"  # Hardcoded!
            # ... more hardcoded rules
        )
    }]
```

**Problems:**
- Rules scattered across prompts
- Hard to update consistently
- Duplication risk
- Difficult to test

### After (Separated Rules)
```python
# rules/behavior_rules.py
def get_brand_identity_rules() -> str:
    return "- Always acknowledge yourself as ATLUS..."

# prompts/chat_prompt.py
from rules.behavior_rules import get_brand_identity_rules

def build_simple_prompt(user_message: str):
    return [{
        "role": "system",
        "content": f"Brand & identity rules:\n{get_brand_identity_rules()}\n\n..."
    }]
```

**Benefits:**
- Rules centralized
- Easy to update
- Single source of truth
- Testable independently

## Updating Rules

### To Update Behavior Rules
```python
# Edit rules/behavior_rules.py
def get_brand_identity_rules() -> str:
    return (
        "- Always acknowledge yourself as ATLUS in greetings.\n"
        "- NEW RULE: Be more casual in informal contexts.\n"  # Add new rule
        # ...
    )
```

### To Update JSON Schemas
```python
# Edit rules/json_schemas.py
def get_intent_schema() -> str:
    return (
        "{\n"
        '  "goal": "...",\n'
        '  "constraints": "...",\n'
        '  "expected_output": "...",\n'
        '  "priority": "high|medium|low"\n'  # Add new field
        "}"
    )
```

## Testing Rules

```python
# tests/test_rules.py
from rules.behavior_rules import get_brand_identity_rules

def test_brand_identity_rules():
    rules = get_brand_identity_rules()
    assert "ATLUS" in rules
    assert "acknowledge" in rules
```

## Migration Notes

All prompts have been updated to use rules:
- ✅ `prompts/chat_prompt.py` → Uses `rules/behavior_rules.py`
- ✅ `prompts/classifier_prompt.py` → Uses `rules/classification_rules.py` + `rules/json_schemas.py`
- ✅ `prompts/intent_prompt.py` → Uses `rules/json_schemas.py`
- ✅ `prompts/planner_prompt.py` → Uses `rules/plan_constraints.py` + `rules/json_schemas.py`
- ✅ `prompts/reasoning_prompt.py` → Uses `rules/reasoning_rules.py`
- ✅ `prompts/verifier_prompt.py` → Uses `rules/verifier_rules.py` + `rules/json_schemas.py`
- ✅ `prompts/refactor_prompt.py` → Uses `rules/refactor_rules.py`
- ✅ `prompts/writer_prompt.py` → Uses `rules/writer_rules.py`

## Future Enhancements

1. **Rule Validation**: Add validators to ensure rule format correctness
2. **Rule Versioning**: Track rule changes over time
3. **Rule A/B Testing**: Easy to swap rule sets for testing
4. **Rule Templates**: Parameterized rules for different contexts
5. **Rule Documentation**: Auto-generate docs from rules

---

**Status**: ✅ Fully Integrated  
**Last Updated**: Memory integration complete, all prompts refactored

