# LLM Unit Tests

This directory contains unit tests for all LLM classes in the ATLUS system.

## Test Files

- `test_intent_llm.py` - Tests for IntentLLM (intent extraction)
- `test_planning_llm.py` - Tests for PlanningLLM (plan generation)
- `test_reasoning_llm.py` - Tests for ReasoningLLM (step-by-step reasoning)
- `test_verifier_llm.py` - Tests for VerifierLLM (verification/critique)
- `test_writer_llm.py` - Tests for WriterLLM (final response writing)
- `conftest.py` - Shared pytest fixtures and configuration

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run a specific test file
```bash
pytest tests/test_intent_llm.py
```

### Run with verbose output
```bash
pytest tests/ -v
```

### Run with coverage
```bash
pytest tests/ --cov=app.llm --cov-report=html
```

### Run a specific test class
```bash
pytest tests/test_intent_llm.py::TestIntentLLM
```

### Run a specific test method
```bash
pytest tests/test_intent_llm.py::TestIntentLLM::test_generate_success
```

## Test Structure

Each test file follows this structure:

1. **Initialization Tests** - Verify LLM classes initialize correctly with proper config
2. **Generation Tests** - Test the `generate()` method with mocked API responses
3. **Configuration Tests** - Verify correct parameters are passed to the API
4. **Edge Cases** - Test empty responses, error handling, etc.

## Mocking

All tests use `unittest.mock` to mock the OpenAI API client, so:
- ✅ No actual API calls are made
- ✅ Tests run fast
- ✅ Tests are deterministic
- ✅ No API keys required for testing

## Dependencies

Tests require:
- `pytest>=7.4.0`
- `pytest-mock>=3.11.1` (optional, for advanced mocking)

Install with:
```bash
pip install -r requirements.txt
```



