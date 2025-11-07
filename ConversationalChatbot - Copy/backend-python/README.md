# Python Flask Backend

This is the backend service for the Conversational Chatbot. It handles message processing and conversation logging.

## Features
- `/chat` endpoint for processing user messages
- Conversation logging to JSON files
- Session management
- Health check endpoint

## Setup

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Service

```bash
python app.py
```

The service will start on `http://localhost:5000`

## API Endpoints

### POST /chat
Process a user message and return a response.

**Request:**
```json
{
  "user_message": "Hello chatbot"
}
```

**Response:**
```json
{
  "assistant_response": "I listened to you: Hello chatbot"
}
```

### GET /health
Check service health and session status.

### POST /reset
Reset the current session and start a new one.

## Output

Conversations are saved to `output/session_<timestamp>.json` with the following format:
```json
{
  "session_id": "20250105_143022",
  "conversations": [
    {"user": "Hello", "assistant": "I listened to you: Hello"},
    {"user": "How are you?", "assistant": "I listened to you: How are you?"}
  ]
}
```
