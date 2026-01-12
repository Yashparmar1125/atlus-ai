# Session API Guide

## Overview

ATLUS now supports explicit session management through dedicated endpoints. Sessions help maintain conversation context, user preferences, and task state across multiple chat interactions.

## Endpoints

### 1. Create Session
**POST** `/api/v1/sessions`

Create a new session for a user.

#### Request
```json
{
    "user_id": "user_123",  // Optional, default: "default_user"
    "metadata": {            // Optional
        "source": "web",
        "client_version": "1.0.0"
    }
}
```

#### Response (201 Created)
```json
{
    "success": true,
    "data": {
        "session_id": "session_a1b2c3d4e5f6",
        "user_id": "user_123",
        "created_at": "2024-01-01T12:00:00Z",
        "metadata": {
            "source": "web",
            "client_version": "1.0.0"
        }
    },
    "timestamp": "2024-01-01T12:00:00Z"
}
```

#### Example
```bash
curl -X POST http://localhost:5000/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "metadata": {"source": "web"}
  }'
```

---

### 2. Get Session Info
**GET** `/api/v1/sessions/{session_id}`

Get detailed information about a session, including memory statistics.

#### Response (200 OK)
```json
{
    "success": true,
    "data": {
        "session_id": "session_a1b2c3d4e5f6",
        "user_id": "user_123",
        "created_at": "2024-01-01T12:00:00Z",
        "last_activity": "2024-01-01T12:30:00Z",
        "is_active": true,
        "metadata": {
            "source": "web"
        },
        "memory": {
            "session_id": "session_a1b2c3d4e5f6",
            "has_session_memory": true,
            "has_working_memory": true,
            "has_behavior_profile": true,
            "conversation_turns": 5
        }
    },
    "timestamp": "2024-01-01T12:30:00Z"
}
```

#### Example
```bash
curl -X GET http://localhost:5000/api/v1/sessions/session_a1b2c3d4e5f6
```

---

### 3. Delete Session
**DELETE** `/api/v1/sessions/{session_id}`

Terminate and delete a session. This clears all session memory and data.

#### Response (200 OK)
```json
{
    "success": true,
    "message": "Session deleted successfully",
    "session_id": "session_a1b2c3d4e5f6",
    "timestamp": "2024-01-01T12:35:00Z"
}
```

#### Example
```bash
curl -X DELETE http://localhost:5000/api/v1/sessions/session_a1b2c3d4e5f6
```

---

### 4. Chat Endpoint (Updated)
**POST** `/api/v1/chat`

Send a chat message. Now supports session validation.

#### Request
```json
{
    "message": "Hello, ATLUS!",
    "session_id": "session_a1b2c3d4e5f6",  // Recommended - from /sessions endpoint
    "user_id": "user_123",                  // Optional
    "metadata": {}                          // Optional
}
```

#### Response (200 OK)
```json
{
    "success": true,
    "data": {
        "response": "Hello! How can I help you today?",
        "session_id": "session_a1b2c3d4e5f6",
        "execution_time": 1.23,
        "request_id": "req_1234567890"
    },
    "timestamp": "2024-01-01T12:00:00Z"
}
```

**Note:**
- If `session_id` is provided, it will be validated
- If `session_id` is not provided, a temporary session will be created (backward compatible)
- **Recommended**: Create a session first using `/sessions` endpoint

---

## Usage Flow

### Recommended Flow

1. **Create Session**
   ```bash
   POST /api/v1/sessions
   → Receive session_id
   ```

2. **Use Session for Chat**
   ```bash
   POST /api/v1/chat
   {
       "message": "Hello",
       "session_id": "<session_id from step 1>"
   }
   ```

3. **Continue Conversation**
   ```bash
   POST /api/v1/chat
   {
       "message": "What did I just say?",
       "session_id": "<same session_id>"
   }
   → ATLUS remembers previous messages
   ```

4. **Check Session Info (Optional)**
   ```bash
   GET /api/v1/sessions/<session_id>
   → See conversation stats, memory info
   ```

5. **Delete Session (When Done)**
   ```bash
   DELETE /api/v1/sessions/<session_id>
   → Clean up session data
   ```

### Example Python Client

```python
import requests

BASE_URL = "http://localhost:5000/api/v1"

# 1. Create session
response = requests.post(f"{BASE_URL}/sessions", json={
    "user_id": "user_123",
    "metadata": {"source": "python_client"}
})
session_data = response.json()["data"]
session_id = session_data["session_id"]
print(f"Created session: {session_id}")

# 2. Send first message
response = requests.post(f"{BASE_URL}/chat", json={
    "message": "Hi, my name is John",
    "session_id": session_id
})
print(response.json()["data"]["response"])

# 3. Send second message (ATLUS remembers)
response = requests.post(f"{BASE_URL}/chat", json={
    "message": "What's my name?",
    "session_id": session_id
})
print(response.json()["data"]["response"])
# → "Your name is John"

# 4. Get session info
response = requests.get(f"{BASE_URL}/sessions/{session_id}")
print(response.json()["data"]["memory"]["conversation_turns"])

# 5. Delete session
response = requests.delete(f"{BASE_URL}/sessions/{session_id}")
print(response.json()["message"])
```

---

## Session Features

### Automatic Memory Initialization
When a session is created, all memory components are automatically initialized:
- **Session Memory**: For conversation history
- **Working Memory**: For task-level decisions
- **Behavior Profile**: For interaction style

### Session Validation
- Sessions are validated when used in chat endpoint
- Invalid or inactive sessions return 404 error
- Session activity is automatically tracked

### Session Activity Tracking
- Last activity timestamp is updated on each chat request
- Useful for session expiration (future feature)

### Memory Statistics
- Get session info to see:
  - Conversation turns count
  - Memory component status
  - Session metadata

---

## Error Handling

### Invalid Session
```json
{
    "success": false,
    "error": {
        "code": "INVALID_SESSION",
        "message": "Invalid or inactive session: session_xxx"
    },
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### Session Not Found
```json
{
    "success": false,
    "error": {
        "code": "SESSION_NOT_FOUND",
        "message": "Session session_xxx not found"
    },
    "timestamp": "2024-01-01T12:00:00Z"
}
```

---

## Best Practices

1. **Always create sessions explicitly** for production applications
2. **Store session_id** client-side (cookie, localStorage, etc.)
3. **Reuse session_id** across chat requests for conversation continuity
4. **Delete sessions** when user logs out or session is no longer needed
5. **Use metadata** to track session source, client version, etc.
6. **Check session info** periodically to monitor conversation state

---

## Implementation Details

### Session ID Format
- Prefix: `session_`
- Format: `session_{16_hex_chars}`
- Example: `session_a1b2c3d4e5f67890`

### Session Storage
- **Development**: In-memory Python dictionaries
- **Production**: Use Redis or database (recommended)

### Session Lifecycle
1. **Created**: Session initialized with memory components
2. **Active**: Session validated and used for chat
3. **Updated**: Activity timestamp updated on each use
4. **Deleted**: Session and all memory cleared

---

## Migration Notes

### Backward Compatibility
- Chat endpoint still works without `session_id` (creates temporary session)
- Existing code will continue to work
- Recommended to migrate to explicit session creation

### Changes
- ✅ New `/sessions` endpoint for session management
- ✅ Session validation in chat endpoint
- ✅ Session activity tracking
- ✅ Session info endpoint with memory stats
- ✅ Session deletion endpoint

---

**Status**: ✅ Fully Integrated  
**Last Updated**: Session API complete with full lifecycle management

