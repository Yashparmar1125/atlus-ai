# Continue Session API

## Endpoint

**GET** `/api/v1/sessions/continue`

Get the last active session for a user to continue the conversation.

## Request

### Query Parameters
- `user_id` (optional): User identifier. Default: `"default_user"`

### Example
```bash
GET /api/v1/sessions/continue?user_id=user_123
```

## Response

### Success (200 OK)
```json
{
    "success": true,
    "data": {
        "session_id": "session_abc123...",
        "user_id": "user_123",
        "created_at": "2024-01-01T12:00:00Z",
        "last_activity": "2024-01-01T12:30:00Z",
        "is_active": true,
        "metadata": {
            "source": "web"
        }
    },
    "timestamp": "2024-01-01T12:35:00Z"
}
```

### Not Found (404)
```json
{
    "success": false,
    "error": {
        "code": "NO_SESSION_FOUND",
        "message": "No active session found for user: user_123"
    },
    "timestamp": "2024-01-01T12:35:00Z"
}
```

## Usage Flow

### 1. Continue Last Session
```bash
# Get last session for user
curl -X GET "http://localhost:5000/api/v1/sessions/continue?user_id=user_123"

# Response contains session_id to use
```

### 2. Use Session for Chat
```bash
# Use the session_id from step 1
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What did we discuss earlier?",
    "session_id": "session_abc123..."
  }'
```

## Python Example

```python
import requests

BASE_URL = "http://localhost:5000/api/v1"

# Get last session
response = requests.get(f"{BASE_URL}/sessions/continue", params={"user_id": "user_123"})

if response.status_code == 200:
    data = response.json()["data"]
    session_id = data["session_id"]
    
    # Continue conversation
    response = requests.post(f"{BASE_URL}/chat", json={
        "message": "What did we discuss?",
        "session_id": session_id
    })
    print(response.json()["data"]["response"])
else:
    # No session found, create a new one
    response = requests.post(f"{BASE_URL}/sessions", json={"user_id": "user_123"})
    session_id = response.json()["data"]["session_id"]
```

## Behavior

- Returns the **most recent active session** for the user
- Sessions are sorted by `last_activity` timestamp (most recent first)
- Only returns **active** sessions (`is_active: true`)
- Returns `404` if no active sessions found for the user

## Use Cases

1. **Resume Conversation**: User returns to the app and wants to continue previous conversation
2. **Multi-Device Sync**: Get the same session across devices
3. **Session Recovery**: Find the last session if session_id was lost
4. **Analytics**: Track which sessions users continue

## Implementation Details

- Uses `SessionService.get_last_session(user_id)` method
- Searches through all active sessions for the user
- Sorts by `last_activity` timestamp (descending)
- Returns the most recent session

---

**Status**: ✅ Implemented and Ready to Use

