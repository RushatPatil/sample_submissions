# Architecture Documentation

## System Overview

ConversationalChatbot-CLI is a microservices-based chatbot system with three independent components:

1. **Frontend**: React 18 web application
2. **Orchestrator**: Java 17 Spring Boot middleware
3. **Backend**: Python 3.11+ CLI application

## Architecture Diagram

```
┌──────────────────────────────────────┐
│         User Browser                  │
│      http://localhost:3000           │
└──────────────┬───────────────────────┘
               │
               │ HTTP POST /api/message
               │ {"message": "Hello"}
               │
               ▼
┌──────────────────────────────────────┐
│   React Frontend (Port 3000)          │
│   - Chat UI                           │
│   - Message state management          │
│   - API client                        │
└──────────────┬───────────────────────┘
               │
               │ HTTP POST /api/message
               │ Content-Type: application/json
               │
               ▼
┌──────────────────────────────────────┐
│   Java Orchestrator (Port 8080)       │
│   ┌──────────────────────────────┐   │
│   │  ChatController              │   │
│   │  - @PostMapping /api/message │   │
│   │  - Validation                │   │
│   └──────────┬───────────────────┘   │
│              │                        │
│              ▼                        │
│   ┌──────────────────────────────┐   │
│   │  ChatService                 │   │
│   │  - ProcessBuilder            │   │
│   │  - JSON parsing              │   │
│   │  - Transaction logging       │   │
│   └──────────┬───────────────────┘   │
└──────────────┼───────────────────────┘
               │
               │ ProcessBuilder.start()
               │ Command: python chatbot_cli.py -m "Hello"
               │
               ▼
┌──────────────────────────────────────┐
│   Python CLI Backend                  │
│   ┌──────────────────────────────┐   │
│   │  ChatbotCLI class            │   │
│   │  - process_message()         │   │
│   │  - save_conversation()       │   │
│   └──────────┬───────────────────┘   │
│              │                        │
│              ▼                        │
│   ┌──────────────────────────────┐   │
│   │  stdout                      │   │
│   │  {"assistant_response": "..."│   │
│   └──────────────────────────────┘   │
│              │                        │
│              ▼                        │
│   ┌──────────────────────────────┐   │
│   │  File: output/session_*.json │   │
│   └──────────────────────────────┘   │
└──────────────────────────────────────┘
```

## Data Flow

### Request Flow (User → Assistant)

1. **User Input**
   - User types message in React UI
   - Message stored in React state

2. **Frontend Processing**
   - React validates non-empty message
   - Sends HTTP POST to Java orchestrator
   - Shows loading indicator

3. **Orchestrator Receives**
   - ChatController validates request
   - Logs incoming message to file
   - Passes to ChatService

4. **CLI Execution**
   - ChatService builds command:
     ```bash
     python chatbot_cli.py -m "user message"
     ```
   - ProcessBuilder executes Python CLI
   - Separate threads read stdout and stderr

5. **CLI Processing**
   - Python CLI receives message via argument
   - Processes message (simple echo logic)
   - Saves to JSON file
   - Outputs JSON to stdout:
     ```json
     {"assistant_response": "I listened to you: user message"}
     ```

6. **Orchestrator Parses**
   - ChatService reads stdout
   - Parses JSON response
   - Extracts assistant_response
   - Logs outgoing message

7. **Frontend Displays**
   - React receives JSON response
   - Adds assistant message to chat
   - Scrolls to bottom
   - Hides loading indicator

### Error Flow

```
Error Source → Detection → Logging → Response
```

**Python CLI Error:**
```
Python Exception
  ↓
Exit code ≠ 0 or JSON with "error" key
  ↓
Java logs error
  ↓
Returns 500 error to React
  ↓
React displays error message in chat
```

**Java Processing Error:**
```
ProcessBuilder exception
  ↓
ChatService catches exception
  ↓
Logs to orchestrator.log
  ↓
Returns 500 error to React
  ↓
React displays error message
```

**Network Error:**
```
React fetch() fails
  ↓
Catch block in sendMessage()
  ↓
Display error in chat with connection details
```

## Component Details

### 1. React Frontend

**Technology Stack:**
- React 18.2
- Modern React Hooks (useState, useEffect, useRef)
- Fetch API for HTTP requests

**Key Files:**
- `src/App.js` - Main component with chat logic
- `src/App.css` - Styling and layout
- `src/index.js` - Application entry point

**State Management:**
```javascript
const [messages, setMessages] = useState([])      // Chat history
const [inputMessage, setInputMessage] = useState('') // Current input
const [isLoading, setIsLoading] = useState(false)  // Loading state
```

**API Integration:**
```javascript
fetch('http://localhost:8080/api/message', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: userMessage })
})
```

### 2. Java Orchestrator

**Technology Stack:**
- Spring Boot 3.2
- Java 17
- Jackson for JSON
- Lombok for DTOs

**Key Classes:**

**OrchestratorApplication.java**
```java
@SpringBootApplication
public class OrchestratorApplication {
    // Main entry point, starts Spring Boot
}
```

**ChatController.java**
```java
@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class ChatController {
    @PostMapping("/message")  // Receives requests from React
    @GetMapping("/health")    // Health check endpoint
}
```

**ChatService.java**
```java
@Service
public class ChatService {
    public String processMessage(String userMessage) {
        // 1. Build ProcessBuilder command
        // 2. Execute Python CLI
        // 3. Read stdout (JSON response)
        // 4. Read stderr (logs)
        // 5. Parse JSON
        // 6. Log transaction
        // 7. Return response
    }
}
```

**Process Execution:**
```java
ProcessBuilder pb = new ProcessBuilder(
    "python",
    "chatbot_cli.py",
    "-m",
    userMessage
);
pb.directory(new File(cliDirectory));
Process process = pb.start();
```

**Output Handling:**
```java
// stdout → JSON response
BufferedReader stdout = new BufferedReader(
    new InputStreamReader(process.getInputStream())
);

// stderr → logs (separate thread)
BufferedReader stderr = new BufferedReader(
    new InputStreamReader(process.getErrorStream())
);
```

### 3. Python CLI Backend

**Technology Stack:**
- Python 3.11+
- Standard library only (json, os, sys, argparse, pathlib, datetime)
- Type hints for modern Python

**Key Components:**

**ChatbotCLI Class:**
```python
class ChatbotCLI:
    def __init__(self, output_dir: str = "output")
    def process_message(self, user_message: str) -> Dict[str, str]
    def _save_conversation(self) -> None
    def interactive_mode(self) -> None
    def single_message_mode(self, message: str) -> None
```

**Modes of Operation:**

1. **Single Message Mode** (Java integration)
   ```bash
   python chatbot_cli.py -m "Hello"
   # Output: {"assistant_response": "I listened to you: Hello"}
   ```

2. **Interactive Mode** (Human testing)
   ```bash
   python chatbot_cli.py -i
   # Starts interactive chat session
   ```

3. **Stdin Mode** (Pipe support)
   ```bash
   echo "Hello" | python chatbot_cli.py
   ```

4. **Health Check**
   ```bash
   python chatbot_cli.py --health
   ```

**Output Separation:**
- **stdout**: Clean JSON only (for Java parsing)
- **stderr**: Logs, timestamps, debug info

## Communication Protocol

### Frontend ↔ Orchestrator

**Protocol:** HTTP REST
**Format:** JSON
**Port:** 8080

**Request:**
```json
POST /api/message
Content-Type: application/json

{
  "message": "user message here"
}
```

**Response (Success):**
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "response": "I listened to you: user message here"
}
```

**Response (Error):**
```json
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "response": "Message cannot be empty"
}
```

### Orchestrator ↔ CLI

**Protocol:** Process execution
**Format:** Command-line arguments + JSON stdout
**Communication:** stdin/stdout/stderr

**Invocation:**
```bash
python chatbot_cli.py -m "user message"
```

**CLI Output (stdout):**
```json
{"assistant_response": "I listened to you: user message"}
```

**CLI Logs (stderr):**
```
[2025-01-06 14:30:22] User: user message
[2025-01-06 14:30:22] Assistant: I listened to you: user message
[LOG] Conversation saved to: output/session_20250106_143022.json
```

## Logging Strategy

### Three-Tier Logging

1. **React Browser Console**
   - User interactions
   - API requests/responses
   - JavaScript errors

2. **Java Orchestrator Logs**
   - File: `orchestrator-java/logs/orchestrator.log`
   - Format: `[timestamp] TYPE: message`
   - Content: All incoming/outgoing transactions + errors

   Example:
   ```
   [2025-01-06 14:30:22] INCOMING: Hello
   [2025-01-06 14:30:22] OUTGOING: I listened to you: Hello
   ```

3. **Python CLI Logs**
   - File: `backend-python-cli/output/session_*.json`
   - Format: Structured JSON
   - Content: Complete conversation history

   Example:
   ```json
   {
     "session_id": "20250106_143022",
     "conversations": [
       {
         "user": "Hello",
         "assistant": "I listened to you: Hello",
         "timestamp": "2025-01-06T14:30:22.123456"
       }
     ]
   }
   ```

## Configuration

### Orchestrator Configuration

**File:** `orchestrator-java/src/main/resources/application.properties`

```properties
# Server
server.port=8080

# Python CLI Integration
python.cli.path=../backend-python-cli/chatbot_cli.py
python.executable=python

# Logging
logging.level.com.chatbot.orchestrator=DEBUG
```

### Environment-Specific Config

**Development:**
```properties
python.executable=python
python.cli.path=../backend-python-cli/chatbot_cli.py
```

**Production:**
```properties
python.executable=/usr/bin/python3.11
python.cli.path=/opt/chatbot/backend-python-cli/chatbot_cli.py
```

**Windows:**
```properties
python.executable=C:\\Python311\\python.exe
python.cli.path=C:\\chatbot\\backend-python-cli\\chatbot_cli.py
```

## Error Handling

### Error Types and Responses

| Error Type | Detection | Response | User Experience |
|------------|-----------|----------|----------------|
| Empty message | React validation | Blocked before send | Send button disabled |
| Network error | Fetch failure | Error message in chat | Red error bubble |
| CLI not found | ProcessBuilder | 500 error | "Error processing message" |
| CLI timeout | Process.waitFor | 500 error | "Error processing message" |
| CLI error | Exit code ≠ 0 | 500 error | "Error processing message" |
| JSON parse error | ObjectMapper | 500 error | "Error processing message" |

### Timeout Handling

```java
// 10-second timeout for CLI execution
boolean finished = process.waitFor(10, TimeUnit.SECONDS);
if (!finished) {
    process.destroyForcibly();
    throw new RuntimeException("Python CLI process timed out");
}
```

## Performance Characteristics

### Latency Breakdown

Typical request (measured):
```
User types → React state update: <10ms
React → Java HTTP: 10-30ms
Java → Python CLI startup: 100-500ms
Python processing: <10ms
Python → Java response: <10ms
Java → React HTTP: 10-30ms
React rendering: <10ms
─────────────────────────────────
Total: 140-600ms (avg ~300ms)
```

### Bottlenecks

1. **Python Interpreter Startup** (~100-500ms)
   - Major contributor to latency
   - Happens on every request
   - Mitigation: Use persistent process

2. **Process Creation Overhead** (~50-100ms)
   - OS overhead for spawning process
   - Mitigation: Process pooling

3. **JSON Parsing** (<10ms)
   - Minimal overhead
   - No optimization needed

### Concurrency Model

- **React**: Single-threaded (JavaScript event loop)
- **Java**: Multi-threaded (Spring Boot defaults to 200 threads)
- **Python CLI**: One process per request

**Concurrent Requests:**
- 10 users → 10 Python processes
- Each isolated from others
- No shared state issues

## Security Considerations

### Current Implementation

1. **CORS**: Open to all origins (`*`)
   - **Risk**: Any website can call the API
   - **Mitigation**: Restrict in production

2. **Input Validation**: Minimal
   - **Risk**: Command injection via message
   - **Mitigation**: Use ProcessBuilder (not shell), sanitize input

3. **Process Execution**: Direct Python invocation
   - **Risk**: Path traversal in python.cli.path
   - **Mitigation**: Validate path, use absolute paths

### Production Hardening

```properties
# 1. Restrict CORS
@CrossOrigin(origins = "https://yourdomain.com")

# 2. Add authentication
# Implement Spring Security

# 3. Rate limiting
# Add request throttling

# 4. Input sanitization
# Validate and escape user input

# 5. Process isolation
# Run CLI in sandboxed environment
```

## Scalability

### Current Limitations

1. **Process Overhead**: Each request spawns new process
2. **No Caching**: Repeated messages processed fresh
3. **File I/O**: Every message writes to disk
4. **No Load Balancing**: Single orchestrator instance

### Scaling Strategies

**Horizontal Scaling:**
```
Load Balancer
    ↓
┌─────────┬─────────┬─────────┐
│ Java 1  │ Java 2  │ Java 3  │
└─────────┴─────────┴─────────┘
    ↓           ↓           ↓
  Python      Python      Python
  Processes   Processes   Processes
```

**Vertical Scaling:**
- Increase JVM heap size
- More CPU cores for concurrent processes
- Faster disk for logs

**Optimization:**
1. Keep Python process alive (socket communication)
2. Cache responses for repeated messages
3. Batch conversation saves
4. Use message queue (RabbitMQ, Kafka)

## Comparison: Flask vs CLI

### Architecture Differences

| Aspect | Flask Version | CLI Version |
|--------|--------------|-------------|
| **Backend Type** | Long-running server | Per-request process |
| **Communication** | HTTP REST | Process execution |
| **State** | In-memory session | File-based |
| **Concurrency** | Thread pool | Process isolation |
| **Startup** | Once at server start | Per request |
| **Latency** | ~50-100ms | ~140-600ms |
| **Dependencies** | Flask, flask-cors | None |
| **Deployment** | Need port 5000 | No port needed |

### Code Differences

**Flask Backend:**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    response = process_message(data['user_message'])
    return jsonify({"assistant_response": response})

app.run(port=5000)
```

**CLI Backend:**
```python
import sys
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--message')
    args = parser.parse_args()

    response = process_message(args.message)
    print(json.dumps({"assistant_response": response}))

if __name__ == "__main__":
    main()
```

**Java Integration - Flask:**
```java
RestTemplate restTemplate = new RestTemplate();
ResponseEntity<PythonResponse> response = restTemplate.postForEntity(
    "http://localhost:5000/chat",
    request,
    PythonResponse.class
);
```

**Java Integration - CLI:**
```java
ProcessBuilder pb = new ProcessBuilder("python", "chatbot_cli.py", "-m", message);
Process process = pb.start();
BufferedReader reader = new BufferedReader(
    new InputStreamReader(process.getInputStream())
);
String jsonResponse = reader.readLine();
```

## Testing Strategy

### Unit Testing

**React:**
```javascript
test('sends message on button click', () => {
    render(<App />);
    // Test component behavior
});
```

**Java:**
```java
@Test
public void testProcessMessage() {
    String response = chatService.processMessage("test");
    assertNotNull(response);
}
```

**Python:**
```python
def test_process_message():
    cli = ChatbotCLI()
    result = cli.process_message("test")
    assert "assistant_response" in result
```

### Integration Testing

```bash
# 1. Start Java orchestrator
cd orchestrator-java && mvn spring-boot:run &

# 2. Test end-to-end
curl -X POST http://localhost:8080/api/message \
  -H "Content-Type: application/json" \
  -d '{"message": "integration test"}'

# 3. Verify response
# Should return: {"response": "I listened to you: integration test"}
```

---

**Document Version:** 1.0
**Last Updated:** 2025
**Author:** ConversationalChatbot-CLI Team
