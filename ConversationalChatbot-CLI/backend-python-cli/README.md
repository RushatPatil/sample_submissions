# Python CLI Backend

This is the CLI-based backend service for the Conversational Chatbot. It processes chat messages through a command-line interface instead of a web API.

## Features

- Command-line interface for message processing
- Multiple operation modes: single message, interactive, and stdin
- Conversation logging to JSON files
- Session management with timestamps
- Health check support
- Python 3.11+ compatible
- No external dependencies (uses Python standard library only)

## Requirements

- Python 3.11 or higher

## Installation

No installation required! The CLI uses only Python's standard library.

```bash
# Optional: Create a virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate
```

## Usage

### 1. Single Message Mode (for Java integration)

Process a single message and output JSON response:

```bash
python chatbot_cli.py -m "Hello chatbot"
```

**Output:**
```json
{"assistant_response": "I listened to you: Hello chatbot"}
```

### 2. Interactive Mode

Run an interactive chat session:

```bash
python chatbot_cli.py -i
```

or simply:

```bash
python chatbot_cli.py
```

**Example:**
```
==================================================
Conversational Chatbot CLI
Session ID: 20250106_143022
Type 'exit' or 'quit' to end the session
==================================================

You: Hello
Assistant: I listened to you: Hello
You: How are you?
Assistant: I listened to you: How are you?
You: exit
Goodbye!
```

### 3. Stdin Mode (for piping)

Accept input from stdin:

```bash
echo "Hello from stdin" | python chatbot_cli.py
```

or with JSON input:

```bash
echo '{"user_message": "Hello JSON"}' | python chatbot_cli.py
```

### 4. Health Check

Get health status as JSON:

```bash
python chatbot_cli.py --health
```

**Output:**
```json
{
  "status": "healthy",
  "service": "Python CLI Backend",
  "session_id": "20250106_143022",
  "total_conversations": 5,
  "python_version": "3.11.0 ..."
}
```

## Command-Line Arguments

- `-m, --message <text>`: Process a single message and output JSON
- `-i, --interactive`: Run in interactive mode
- `--health`: Output health status as JSON
- `--output-dir <path>`: Directory to save conversation logs (default: output)

## Output

Conversations are automatically saved to `output/session_<timestamp>.json` with the following format:

```json
{
  "session_id": "20250106_143022",
  "conversations": [
    {
      "user": "Hello",
      "assistant": "I listened to you: Hello",
      "timestamp": "2025-01-06T14:30:22.123456"
    },
    {
      "user": "How are you?",
      "assistant": "I listened to you: How are you?",
      "timestamp": "2025-01-06T14:30:28.654321"
    }
  ]
}
```

## Integration with Java

The Java orchestrator calls this CLI using ProcessBuilder:

```java
ProcessBuilder pb = new ProcessBuilder(
    "python", "chatbot_cli.py", "-m", userMessage
);
Process process = pb.start();
// Read JSON from stdout
```

## Logging

- **stdout**: Contains only JSON responses (clean for Java parsing)
- **stderr**: Contains logs, timestamps, and debug information
- **Files**: Conversations saved to `output/session_*.json`

## Examples

### Java Integration Example

```java
String pythonScript = "path/to/chatbot_cli.py";
String message = "Hello chatbot";

ProcessBuilder pb = new ProcessBuilder("python", pythonScript, "-m", message);
Process process = pb.start();

BufferedReader reader = new BufferedReader(
    new InputStreamReader(process.getInputStream())
);
String jsonResponse = reader.readLine();
// Parse jsonResponse as JSON
```

### Testing

```bash
# Test single message
python chatbot_cli.py -m "Test message"

# Test health check
python chatbot_cli.py --health

# Test interactive mode
python chatbot_cli.py -i

# Test stdin JSON
echo '{"user_message": "Test"}' | python chatbot_cli.py

# Test stdin plain text
echo "Plain text test" | python chatbot_cli.py
```

## Error Handling

Errors are returned as JSON:

```json
{"error": "error message here"}
```

## File Structure

```
backend-python-cli/
├── chatbot_cli.py          # Main CLI application
├── requirements.txt         # Dependencies (empty - uses stdlib)
├── README.md               # This file
└── output/                 # Conversation logs
    └── session_*.json      # Session files
```

## Differences from Flask Version

| Feature | Flask Version | CLI Version |
|---------|--------------|-------------|
| Interface | HTTP REST API | Command-line |
| Port | 5000 | N/A |
| Dependencies | Flask, flask-cors | None (stdlib only) |
| Invocation | HTTP POST | Process execution |
| Output | HTTP JSON response | stdout JSON |
| Python Version | 3.8+ | 3.11+ |

## Python Version

This CLI is designed for Python 3.11+ and uses modern Python features:
- Type hints with `from typing import`
- Path operations with `pathlib`
- String type annotations
- Modern exception handling

## Troubleshooting

### Python not found
Ensure Python 3.11+ is installed and in your PATH:
```bash
python --version
```

### Permission denied (Linux/Mac)
Make the script executable:
```bash
chmod +x chatbot_cli.py
./chatbot_cli.py -m "Hello"
```

### JSON parsing errors
Ensure you're reading only stdout (not stderr) in your Java code:
```java
process.getInputStream()  // stdout - JSON output
process.getErrorStream()  // stderr - logs
```

## Future Enhancements

Possible improvements:
- Add authentication/API key support
- Implement colored output for interactive mode
- Add conversation history retrieval
- Support for conversation context/memory
- Add rate limiting
- Implement logging levels (debug, info, error)
