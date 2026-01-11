# Logging Guide for ATLUS Agent

## Overview

The ATLUS agent now includes comprehensive logging that tracks every step of the execution pipeline. All logs are written to files with rotation support.

## Log File Location

- **Directory**: `logs/` (created automatically)
- **Main log file**: `logs/atlus.log`
- **Rotation**: Logs rotate when they reach 10MB
- **Backups**: Keeps 5 backup files (atlus.log.1, atlus.log.2, etc.)

## Log Levels

- **DEBUG**: Detailed information for debugging (file only)
- **INFO**: General information about execution flow (file + console)
- **WARNING**: Non-critical issues (file + console)
- **ERROR**: Critical errors with full stack traces (file + console)

## What Gets Logged

### 1. Agent Initialization
- LLM instance creation
- Initialization status

### 2. Intent Extraction
- User input message
- Prompt building
- LLM API calls with timing
- Raw responses (preview)
- Parsing and validation attempts
- Retry attempts and repairs
- Final extracted intent

### 3. Planning
- Intent JSON passed to planner
- LLM API calls with timing
- Raw plan responses (preview)
- Parsing and validation
- Number of plan steps
- Individual step details

### 4. Reasoning
- Context formatting
- Plan step count
- Prompt building
- LLM generation timing
- Draft length and preview

### 5. Verification
- Draft length
- Verifier API calls with timing
- Issues and fixes count
- Parsed verification results

### 6. Refactoring
- Original draft length
- Issues and fixes count
- Refactoring timing
- Length changes

### 7. Final Writing
- Refactored draft length
- Writer API calls with timing
- Final response length and preview

### 8. Execution Summary
- Total execution time
- Final response length
- Success/failure status

### 9. Error Handling
- Full exception stack traces
- Error context
- Execution time before failure

## Log Format

### File Logs (Detailed)
```
2024-01-15 14:30:25 | INFO     | atlus.agent | run:56 | AGENT EXECUTION STARTED
2024-01-15 14:30:25 | INFO     | atlus.agent | run:58 | User Input: Build a web app
2024-01-15 14:30:25 | DEBUG    | atlus.agent | _safe_intent_extraction:82 | Building intent extraction prompt...
2024-01-15 14:30:26 | INFO     | atlus.agent | _safe_intent_extraction:85 | Intent extraction attempt 1/2
2024-01-15 14:30:28 | DEBUG    | atlus.agent | _safe_intent_extraction:89 | LLM response received in 2.15s
```

### Console Logs (Summary)
```
14:30:25 | INFO     | AGENT EXECUTION STARTED
14:30:25 | INFO     | User Input: Build a web app
14:30:25 | INFO     | Intent extraction attempt 1/2
14:30:28 | INFO     | Intent extraction successful on attempt 1
```

## Usage

Logging is automatic when using the Agent class:

```python
from agent.agent import Agent

agent = Agent()  # Logs initialization
result = agent.run("Build a web app")  # Logs entire execution
```

## Configuration

To customize logging, modify `app/utils/logger.py`:

```python
# Change log directory
log_dir = "custom_logs"

# Change log file name
log_file = "my_agent.log"

# Change rotation size (bytes)
max_bytes = 20 * 1024 * 1024  # 20MB

# Change backup count
backup_count = 10

# Change log level
level = logging.INFO  # Only INFO and above
```

## Log Analysis

### Finding Errors
```bash
grep "ERROR" logs/atlus.log
```

### Tracking Execution Times
```bash
grep "execution time" logs/atlus.log
```

### Viewing Recent Activity
```bash
tail -f logs/atlus.log
```

### Finding Specific Steps
```bash
grep "STEP 1" logs/atlus.log
grep "STEP 2" logs/atlus.log
```

## Performance Metrics

The logs include timing information for:
- Each LLM API call
- Each pipeline step
- Total execution time
- Retry attempts

Use these to identify bottlenecks and optimize performance.

## Troubleshooting

### Logs Not Appearing
1. Check if `logs/` directory exists and is writable
2. Verify log level is set appropriately
3. Check file permissions

### Logs Too Verbose
- Set log level to `logging.INFO` in `logger.py`
- DEBUG logs only go to file, not console

### Logs Too Large
- Reduce `max_bytes` for earlier rotation
- Reduce `backup_count` to keep fewer backups
- Consider log cleanup scripts

## Best Practices

1. **Monitor log files regularly** - Check for errors and warnings
2. **Rotate logs** - Don't let logs grow indefinitely
3. **Archive important logs** - Keep logs from production runs
4. **Use log levels appropriately** - DEBUG for development, INFO for production
5. **Review execution times** - Identify slow steps for optimization

