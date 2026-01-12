# Prompt Structure Improvements

## Summary

All prompts that require structured JSON output have been enhanced with:
- **Explicit JSON schema examples**
- **Stronger directive language** ("MUST", "REQUIRED", "CRITICAL")
- **Clear type specifications**
- **Example outputs**
- **Warnings against markdown/explanations**

## Changes Made

### 1. Intent Prompt (`intent_prompt.py`)

**Before:**
- Vague: "Extract and return ONLY valid JSON with: goal, constraints, expected_output"
- No examples
- No type specifications

**After:**
- ✅ Explicit JSON schema with types
- ✅ Complete example output
- ✅ Strong warnings: "CRITICAL: Return ONLY valid JSON. No explanations, no markdown"
- ✅ Clear structure showing constraints can be string or array

**Expected Output:**
```json
{
  "goal": "string",
  "constraints": "string or array",
  "expected_output": "string"
}
```

---

### 2. Planner Prompt (`planner_prompt.py`)

**Before:**
- Vague: "Return JSON with a single key `plan` containing an ordered list of steps"
- No examples
- No validation rules

**After:**
- ✅ Explicit JSON structure with example
- ✅ Rules: minimum 2 steps, maximum 10 steps
- ✅ Clear requirement that steps must be strings
- ✅ Strong warnings about JSON-only output

**Expected Output:**
```json
{
  "plan": [
    "Step 1 description",
    "Step 2 description"
  ]
}
```

---

### 3. Verifier Prompt (`verifier_prompt.py`)

**Before:**
- Vague: "Return JSON with: issues (list), suggested_fixes (list)"
- No examples
- No handling of empty cases

**After:**
- ✅ Explicit JSON structure
- ✅ Examples for both cases (with issues and without)
- ✅ Clear requirement that arrays can be empty
- ✅ Strong warnings about JSON-only output

**Expected Output:**
```json
{
  "issues": ["Issue 1", "Issue 2"],
  "suggested_fixes": ["Fix 1", "Fix 2"]
}
```

---

### 4. Reasoning Prompt (`reasoning_prompt.py`)

**Before:**
- Too brief: "Generate a draft solution"
- No structure guidance

**After:**
- ✅ Clear step-by-step execution instructions
- ✅ Guidance on what to include (explanation, reasoning, solution)
- ✅ Reminder to follow plan strictly

**Note:** This prompt intentionally allows free-form text output (not JSON), as reasoning needs to be flexible.

---

### 5. Writer Prompt (`writer_prompt.py`)

**Status:** ✅ **No changes needed**
- Already well-structured
- Intentionally free-form (final user-facing output)
- Clear rules about what NOT to include

---

## Key Improvements

### 1. **Explicit Schema Examples**
Every JSON-requiring prompt now includes:
- Complete JSON structure
- Type specifications
- Real-world examples

### 2. **Stronger Directives**
- "CRITICAL:" for important requirements
- "MUST" instead of "should"
- "REQUIRED" for mandatory fields
- "ONLY" to prevent extra content

### 3. **Anti-Pattern Warnings**
All JSON prompts now explicitly state:
- "No explanations"
- "No markdown code blocks"
- "No text before or after"
- "Return ONLY the JSON object"

### 4. **Validation Alignment**
Prompts now match the validation logic:
- Intent prompt matches `intent_validator.py` requirements
- Planner prompt matches `plan_parser.py` expectations
- Verifier prompt matches expected structure in `agent.py`

---

## Benefits

1. **Reduced Parse Errors**: Clear examples reduce malformed JSON
2. **Faster Processing**: Less need for repair/retry cycles
3. **Consistency**: All prompts follow the same strict pattern
4. **Maintainability**: Easy to see expected output format

---

## Testing Recommendations

After these changes, verify:
1. ✅ Intent extraction produces valid JSON
2. ✅ Planner produces valid JSON with "plan" array
3. ✅ Verifier produces valid JSON with "issues" and "suggested_fixes"
4. ✅ All outputs parse correctly without repair cycles

Run the agent with various inputs and check:
- Parse success rate
- Number of retries needed
- Output quality



