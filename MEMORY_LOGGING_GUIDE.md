# Memory Logging Guide

## Overview

All memory operations are now logged to separate log files for easy inspection. This allows you to see exactly what's being written to and read from memory.

## Log Files Location

All memory logs are stored in: `logs/memory/`

### Log Files
- `logs/memory/session.log` - Session memory operations (conversation turns)
- `logs/memory/working.log` - Working memory operations (task-level facts)
- `logs/memory/long_term.log` - Long-term memory operations (persistent user data)
- `logs/memory/behavior.log` - Behavior profile operations (interaction style)

## Log Format

Each log entry follows this format:
```
YYYY-MM-DD HH:MM:SS | LEVEL     | OPERATION | key=value | session_id=xxx | user_id=xxx
```

### Example Log Entries

**Session Memory:**
```
2024-01-01 12:00:00 | INFO      | WRITE | key=turn | value=user: Hello... | assistant: Hi!... | session_id=session_abc123
2024-01-01 12:00:05 | INFO      | READ  | key=context | session_id=session_abc123
```

**Working Memory:**
```
2024-01-01 12:00:10 | INFO      | WRITE | key=tech_stack | value=['Python', 'Flask'] | session_id=session_abc123
2024-01-01 12:00:15 | INFO      | READ  | key=tech_stack | session_id=session_abc123
```

**Long-Term Memory:**
```
2024-01-01 12:00:20 | INFO      | WRITE | key=preferred_language | value=Python | user_id=user_123
2024-01-01 12:00:25 | DEBUG     | Saved long-term memory to data/memory_user_123.json (keys: ['preferred_language'])
```

**Behavior Profile:**
```
2024-01-01 12:00:30 | INFO      | WRITE | key=verbosity | value=Verbosity.HIGH
2024-01-01 12:00:35 | INFO      | WRITE | key=tone | value=Tone.TECHNICAL
```

## Operations Logged

### Session Memory
- **WRITE**: When a conversation turn is added (user message + agent response)
- **READ**: When context is retrieved
- Includes: session_id, message previews

### Working Memory
- **WRITE**: When a fact is updated
- **READ**: When facts are retrieved (by key or all)
- Includes: session_id, key, value

### Long-Term Memory
- **WRITE**: When a fact is updated
- **READ**: When facts are retrieved
- **SAVE**: When memory is persisted to disk
- Includes: user_id, key, value, file path

### Behavior Profile
- **WRITE**: When verbosity, tone, or depth is changed
- Includes: key, value

## Viewing Logs

### View Latest Session Memory
```bash
tail -f logs/memory/session.log
```

### View All Memory Operations
```bash
cat logs/memory/*.log | tail -100
```

### Search for Specific Session
```bash
grep "session_abc123" logs/memory/*.log
```

### View Recent Memory Writes
```bash
grep "WRITE" logs/memory/*.log | tail -20
```

## Console Output

- ✅ All operations are logged to files
- ✅ No print statements in console (only logging)
- ✅ Console logs go to main application logs
- ✅ Memory operations go to memory log files

## Log Rotation

Log files will grow over time. Consider:
- Implementing log rotation (future enhancement)
- Clearing old logs periodically
- Using log rotation tools (logrotate, etc.)

## Integration

Memory logging is automatically enabled for:
- Session memory operations
- Working memory operations
- Long-term memory operations
- Behavior profile changes
- MemoryService operations

No code changes needed - logging happens automatically!

---

**Status**: ✅ Memory logging enabled for all memory types

