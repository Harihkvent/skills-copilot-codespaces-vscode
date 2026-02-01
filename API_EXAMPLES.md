# API Usage Examples

This document provides examples of how to use the Astra API.

## Table of Contents
- [Health Check](#health-check)
- [Voice Commands](#voice-commands)
- [Direct Commands](#direct-commands)
- [Tool Examples](#tool-examples)

## Health Check

Check if the API is running and healthy:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Astra API",
  "version": "0.1.0",
  "checks": {
    "database": "healthy",
    "redis": "healthy"
  }
}
```

## Voice Commands

Process a voice command (transcribed text from STT):

```bash
curl -X POST http://localhost:8000/api/v1/voice \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "transcript": "Astra, send an email to ravi@example.com saying I will join the meeting tomorrow",
    "locale": "en-US",
    "context_id": "conv_001"
  }'
```

Response:
```json
{
  "status": "requires_confirmation",
  "task_id": "task_abc123",
  "estimated_ops": ["mail.send"],
  "message": "This action requires your confirmation. Please confirm to proceed."
}
```

## Direct Commands

Send a text command directly (without STT):

```bash
curl -X POST http://localhost:8000/api/v1/command \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "command": "search the web for Python tutorials",
    "context_id": "conv_001"
  }'
```

Response:
```json
{
  "status": "success",
  "task_id": "task_xyz789",
  "result": {
    "intent": "web_search",
    "results": [...]
  },
  "message": "Command processed successfully"
}
```

## Tool Examples

### Email Tool

Send an email:

```bash
curl -X POST http://localhost:8000/api/v1/command \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "command": "send email to john@example.com with subject Meeting Update and body Hi John, confirming our meeting at 3 PM tomorrow"
  }'
```

### Search Tool

Search the web:

```bash
curl -X POST http://localhost:8000/api/v1/command \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "command": "search for artificial intelligence news"
  }'
```

## Python Client Example

```python
import requests

# API endpoint
BASE_URL = "http://localhost:8000"

# Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Send a command
command_data = {
    "user_id": "user_123",
    "command": "search for machine learning tutorials",
    "context_id": "conv_001"
}

response = requests.post(
    f"{BASE_URL}/api/v1/command",
    json=command_data
)
print(response.json())
```

## JavaScript Client Example

```javascript
// Health check
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Send a command
fetch('http://localhost:8000/api/v1/command', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user_id: 'user_123',
    command: 'search for Python tutorials',
    context_id: 'conv_001'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request (invalid input)
- `401`: Unauthorized (authentication required)
- `500`: Internal Server Error

Example error response:
```json
{
  "detail": "Failed to process command: Database connection error"
}
```

## Authentication (Future)

Authentication will be added in future versions using JWT tokens:

```bash
curl -X POST http://localhost:8000/api/v1/command \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{...}'
```

## WebSocket Support (Future)

Real-time communication will be added via WebSocket:

```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'voice',
    transcript: 'Hello Astra'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Response:', data);
};
```
