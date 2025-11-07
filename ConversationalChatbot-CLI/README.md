# ConversationalChatbot-CLI

A complete multi-component chatbot system demonstrating microservices architecture with **React frontend**, **Java Spring Boot orchestrator**, and **Python CLI backend** (instead of Flask).

This project is a CLI-based variant of the original ConversationalChatbot, where the Python backend has been converted from a Flask REST API to a command-line interface application.

## Key Differences from Original

| Component | Original Version | CLI Version |
|-----------|-----------------|-------------|
| **Python Backend** | Flask REST API (Port 5000) | CLI Application (no port) |
| **Communication** | HTTP POST requests | Process execution |
| **Python Version** | 3.8+ | 3.11+ |
| **Dependencies** | Flask, flask-cors | None (stdlib only) |
| **Java Integration** | RestTemplate HTTP client | ProcessBuilder |
| **Response Format** | HTTP JSON response | stdout JSON output |

## Project Structure

```
ConversationalChatbot-CLI/
│
├── frontend-react/              # React-based UI (Port 3000)
│   ├── src/
│   │   ├── App.js              # Main chat component
│   │   ├── App.css             # Styling
│   │   ├── index.js            # Entry point
│   │   └── index.css
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── README.md
│
├── orchestrator-java/           # Java Spring Boot orchestrator (Port 8080)
│   ├── src/
│   │   └── main/
│   │       ├── java/com/chatbot/orchestrator/
│   │       │   ├── OrchestratorApplication.java
│   │       │   ├── controller/
│   │       │   │   └── ChatController.java
│   │       │   ├── service/
│   │       │   │   └── ChatService.java      # Uses ProcessBuilder
│   │       │   └── model/
│   │       │       ├── MessageRequest.java
│   │       │       └── MessageResponse.java
│   │       └── resources/
│   │           └── application.properties
│   ├── logs/                                   # Transaction logs
│   ├── pom.xml
│   └── README.md
│
└── backend-python-cli/          # Python CLI backend (No port)
    ├── chatbot_cli.py          # CLI application
    ├── requirements.txt         # No dependencies
    ├── output/                  # Conversation logs
    └── README.md
```

## System Architecture

### Original Architecture (Flask)

```
┌─────────────────┐
│  React Frontend │  (Port 3000)
└────────┬────────┘
         │ HTTP POST
         ▼
┌─────────────────┐
│ Java Orchestrator│ (Port 8080)
│   RestTemplate   │
└────────┬────────┘
         │ HTTP POST
         ▼
┌─────────────────┐
│ Python Flask    │  (Port 5000)
│   HTTP Server   │
└─────────────────┘
```

### New Architecture (CLI)

```
┌─────────────────┐
│  React Frontend │  (Port 3000)
└────────┬────────┘
         │ HTTP POST
         ▼
┌─────────────────┐
│ Java Orchestrator│ (Port 8080)
│  ProcessBuilder  │
└────────┬────────┘
         │ Execute: python chatbot_cli.py -m "..."
         ▼
┌─────────────────┐
│  Python CLI     │  (No port)
│  stdout: JSON   │
└─────────────────┘
```

## Features

- **React Frontend**: Modern, responsive chat UI with real-time updates
- **Java Orchestrator**: Middleware service for routing and transaction logging
- **Python CLI Backend**: Command-line message processing and conversation storage
- **Conversation Logging**: All chats saved to JSON files with timestamps
- **Error Handling**: Comprehensive error messages and logging
- **Health Checks**: Service health check endpoints
- **Modern Python**: Python 3.11+ with type hints and modern features
- **No External Dependencies**: Python CLI uses only standard library

## Prerequisites

Make sure you have the following installed:

- **Node.js** 14+ and npm (for React frontend)
- **Java** 17+ and Maven 3.6+ (for Java orchestrator)
- **Python** 3.11+ (for Python CLI backend)

### Verify installations:

```bash
node --version
npm --version
java -version
mvn -version
python --version
```

## Quick Start

### 1. Start the Python CLI (Verify it works)

```bash
cd backend-python-cli

# Test the CLI in interactive mode
python chatbot_cli.py -i

# Or test with a single message
python chatbot_cli.py -m "Hello chatbot"
```

Expected output:
```json
{"assistant_response": "I listened to you: Hello chatbot"}
```

### 2. Start the Java Orchestrator (Port 8080)

Open a new terminal:

```bash
cd orchestrator-java

# Run with Maven
mvn spring-boot:run

# OR build and run the JAR
# mvn clean package
# java -jar target/orchestrator-cli-1.0.0.jar
```

The orchestrator will start on `http://localhost:8080`

**Note:** Ensure the Python CLI path is correctly configured in `orchestrator-java/src/main/resources/application.properties`:
```properties
python.cli.path=../backend-python-cli/chatbot_cli.py
python.executable=python
```

### 3. Start the React Frontend (Port 3000)

Open another new terminal:

```bash
cd frontend-react

# Install dependencies (first time only)
npm install

# Start the development server
npm start
```

The frontend will start on `http://localhost:3000` and open automatically in your browser.

## Usage

1. Open your browser to `http://localhost:3000`
2. Type a message in the input box (e.g., "Hello chatbot")
3. Click "Send" or press Enter
4. The chatbot will respond with: "I listened to you: Hello chatbot"
5. Continue the conversation

## Process Flow Example

**User types:** "Hello chatbot"

1. **React Frontend** → POST to `http://localhost:8080/api/message`
   ```json
   { "message": "Hello chatbot" }
   ```

2. **Java Orchestrator** → Executes Python CLI:
   ```bash
   python chatbot_cli.py -m "Hello chatbot"
   ```

3. **Python CLI** → Outputs to stdout:
   ```json
   { "assistant_response": "I listened to you: Hello chatbot" }
   ```

4. **Java Orchestrator** → Parses JSON and returns to React:
   ```json
   { "response": "I listened to you: Hello chatbot" }
   ```

5. **React Frontend** → Displays the message in the chat window

6. **Python CLI** → Saves conversation to:
   ```
   backend-python-cli/output/session_<timestamp>.json
   ```

## Logging and Output

### Python CLI
- Conversations saved to: `backend-python-cli/output/session_YYYYMMDD_HHMMSS.json`
- stderr logs show timestamps and processing info
- stdout contains only JSON responses (for Java parsing)

### Java Orchestrator
- Transaction logs: `orchestrator-java/logs/orchestrator.log`
- Contains timestamps, request/response details
- Python CLI stderr output (prefixed with `[Python CLI]`)

### React Frontend
- Browser console shows API calls and responses
- Error messages displayed in UI

## Health Checks

Each service provides a health check:

- **React**: Open `http://localhost:3000` (visual check)
- **Java**: GET `http://localhost:8080/api/health`
- **Python CLI**: `python chatbot_cli.py --health`

## Configuration

### Python CLI Configuration

No configuration needed! Uses Python standard library only.

Optional customizations in `chatbot_cli.py`:
- Output directory location
- Response format
- Logging behavior

### Java Orchestrator Configuration

Edit `orchestrator-java/src/main/resources/application.properties`:

```properties
# Server port
server.port=8080

# Python CLI path (relative or absolute)
python.cli.path=../backend-python-cli/chatbot_cli.py

# Python executable (python, python3, or full path)
python.executable=python
```

### React Frontend Configuration

Edit `src/App.js` to change the backend URL:
```javascript
const response = await fetch('http://localhost:8080/api/message', {
```

## Troubleshooting

### Connection Errors

If the frontend shows connection errors:
1. Verify Java orchestrator is running on port 8080
2. Check browser console for detailed error messages
3. Verify CORS is enabled on Java orchestrator

### Python CLI Not Found

Error: `python: command not found`

**Solution:** Ensure Python 3.11+ is in PATH or configure full path:
```properties
python.executable=C:\\Python311\\python.exe
```

### Python Script Not Found

Error: `can't open file 'chatbot_cli.py'`

**Solution:** Verify the path in `application.properties`:
```bash
# Check file exists
ls backend-python-cli/chatbot_cli.py
```

Or use absolute path:
```properties
python.cli.path=C:\\Users\\user\\project\\backend-python-cli\\chatbot_cli.py
```

### Java Not Starting

- Verify Java 17+ is installed: `java -version`
- Check if port 8080 is already in use
- Ensure Maven dependencies are downloaded: `mvn dependency:resolve`

### React Not Starting

- Delete `node_modules` and run `npm install` again
- Clear npm cache: `npm cache clean --force`
- Check if port 3000 is already in use

## Testing Each Component

### Test Python CLI

```bash
cd backend-python-cli

# Single message mode
python chatbot_cli.py -m "Test message"

# Interactive mode
python chatbot_cli.py -i

# Health check
python chatbot_cli.py --health

# Stdin mode
echo "Test" | python chatbot_cli.py
```

### Test Java Orchestrator

```bash
# Health check
curl http://localhost:8080/api/health

# Send message
curl -X POST http://localhost:8080/api/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Test message"}'
```

### Test React Frontend

1. Open http://localhost:3000
2. Open browser developer console (F12)
3. Type a message and send
4. Check network tab for API calls
5. Verify response in console

## Stopping the Services

Press `Ctrl+C` in each terminal to stop the respective service.

## Project Highlights

- **No Flask Dependency**: Pure CLI-based Python backend
- **Modern Python**: Uses Python 3.11+ features (type hints, pathlib)
- **Process-Based Communication**: Java executes Python as subprocess
- **Microservices Architecture**: Three independent, loosely-coupled components
- **RESTful API**: React ↔ Java communication via REST
- **Self-Contained**: All code and configs included
- **Comprehensive Logging**: Full audit trail of all conversations

## Advantages of CLI Approach

1. **No Dependencies**: Python CLI uses only standard library
2. **Simplified Deployment**: No need to run Python web server
3. **Process Isolation**: Each request in separate process
4. **Easy Testing**: Can test CLI directly from command line
5. **Flexible Integration**: Can be called from any language
6. **No Port Conflicts**: Python doesn't need a port

## Disadvantages of CLI Approach

1. **Process Overhead**: Spawning Python process for each request
2. **Startup Latency**: Python interpreter startup time (~100-500ms)
3. **No Persistent State**: Each invocation starts fresh
4. **Limited Concurrency**: Multiple processes for concurrent requests
5. **No Streaming**: Request/response is all-or-nothing

## Performance Considerations

For production use, consider:
- Keep Python CLI process running (persistent mode)
- Use process pool to reduce startup overhead
- Implement caching for repeated requests
- Monitor resource usage (processes, memory)
- Add request queuing and rate limiting

## Future Enhancements

Possible improvements:
- Add authentication and user sessions
- Implement WebSocket for real-time updates
- Add database for conversation persistence
- Persistent Python process (reduce overhead)
- Deploy using Docker containers
- Add unit and integration tests
- Implement rate limiting
- Add message history retrieval
- Process pool for better performance

## Docker Deployment (Future)

Example Dockerfile structure:

```dockerfile
# Multi-stage build for all components
FROM python:3.11 AS python-cli
FROM maven:3-openjdk-17 AS java-build
FROM node:18 AS react-build
```

## Comparison Table

| Aspect | Flask Version | CLI Version |
|--------|--------------|-------------|
| Python Interface | HTTP REST API | Command-line |
| Python Port | 5000 | None |
| Python Dependencies | Flask, flask-cors | None |
| Java HTTP Client | RestTemplate | ProcessBuilder |
| Python Version | 3.8+ | 3.11+ |
| Response Method | HTTP response | stdout JSON |
| Error Method | HTTP status | stderr + exit code |
| Concurrency | Thread-based | Process-based |
| Startup Time | Once (server start) | Per request |
| Testing | curl, Postman | Command line |

## License

This is a demonstration project for educational purposes.

## Contributing

This is a standalone demo project. Feel free to fork and modify for your needs.

---

**Created**: 2025
**Tech Stack**: React 18, Java 17, Spring Boot 3.2, Python 3.11+
**Architecture**: Microservices with CLI integration
**Original Project**: ConversationalChatbot (Flask version)
