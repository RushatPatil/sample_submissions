# Java Orchestrator (CLI Integration)

This is the Java Spring Boot orchestrator service for the CLI-based Conversational Chatbot. It acts as middleware between the React frontend and the Python CLI backend.

## Features

- RESTful API for React frontend communication
- Process-based integration with Python CLI
- Transaction logging to files
- Health check endpoint
- Error handling and timeout management
- Spring Boot 3.2 with Java 17

## Requirements

- Java 17 or higher
- Maven 3.6 or higher
- Python 3.11+ (for CLI backend)

## Configuration

Edit `src/main/resources/application.properties` to configure:

```properties
# Server port
server.port=8080

# Python CLI path (relative or absolute)
python.cli.path=../backend-python-cli/chatbot_cli.py

# Python executable (python, python3, or full path)
python.executable=python
```

## Setup

1. Ensure Java 17+ is installed:
```bash
java -version
```

2. Ensure Maven is installed:
```bash
mvn -version
```

3. Ensure Python CLI is in place:
```bash
# Verify the Python CLI exists
ls ../backend-python-cli/chatbot_cli.py
```

## Running the Service

### Option 1: Run with Maven

```bash
cd orchestrator-java
mvn spring-boot:run
```

### Option 2: Build JAR and run

```bash
cd orchestrator-java

# Build the JAR
mvn clean package

# Run the JAR
java -jar target/orchestrator-cli-1.0.0.jar
```

The orchestrator will start on `http://localhost:8080`

## API Endpoints

### POST /api/message

Process a user message by invoking the Python CLI.

**Request:**
```json
{
  "message": "Hello chatbot"
}
```

**Response:**
```json
{
  "response": "I listened to you: Hello chatbot"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8080/api/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello chatbot"}'
```

### GET /api/health

Check service health and configuration.

**Response:**
```json
{
  "status": "healthy",
  "service": "Java Orchestrator",
  "port": 8080,
  "backend": "Python CLI"
}
```

**cURL Example:**
```bash
curl http://localhost:8080/api/health
```

## How It Works

1. **React frontend** sends HTTP POST to `/api/message`
2. **ChatController** receives the request and validates it
3. **ChatService** executes the Python CLI using ProcessBuilder:
   ```
   python chatbot_cli.py -m "user message"
   ```
4. Python CLI outputs JSON to stdout:
   ```json
   {"assistant_response": "..."}
   ```
5. **ChatService** parses the JSON and extracts the response
6. Response is returned to React frontend
7. Transaction is logged to `logs/orchestrator.log`

## Process Flow

```
┌─────────────────┐
│  React Frontend │
│   (Port 3000)   │
└────────┬────────┘
         │ HTTP POST /api/message
         │ {"message": "..."}
         ▼
┌─────────────────┐
│ ChatController  │
│  @PostMapping   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ChatService    │
│  ProcessBuilder │
└────────┬────────┘
         │ Execute: python chatbot_cli.py -m "..."
         ▼
┌─────────────────┐
│  Python CLI     │
│  stdout: JSON   │
│  stderr: logs   │
└─────────────────┘
```

## Logging

### Transaction Logs

All incoming requests and outgoing responses are logged to:
```
orchestrator-java/logs/orchestrator.log
```

Format:
```
[2025-01-06 14:30:22] INCOMING: Hello chatbot
[2025-01-06 14:30:22] OUTGOING: I listened to you: Hello chatbot
```

### Console Logs

- Application startup information
- Python CLI execution details
- Python CLI stderr output (prefixed with `[Python CLI]`)
- Errors and exceptions

## Error Handling

The orchestrator handles various error scenarios:

1. **Empty message**: Returns 400 Bad Request
2. **CLI process timeout**: Process killed after 10 seconds
3. **CLI execution failure**: Returns error with exit code
4. **CLI returns error JSON**: Extracts and reports the error
5. **Empty CLI response**: Reports missing output

All errors are logged to `logs/orchestrator.log` and returned to the frontend.

## Configuration Options

### Python Executable

If Python is not in PATH or you need a specific version:

```properties
# Use python3 explicitly
python.executable=python3

# Use full path
python.executable=/usr/bin/python3.11

# Windows full path
python.executable=C:\\Python311\\python.exe
```

### CLI Path

```properties
# Relative path (default)
python.cli.path=../backend-python-cli/chatbot_cli.py

# Absolute path (Linux/Mac)
python.cli.path=/home/user/chatbot/backend-python-cli/chatbot_cli.py

# Absolute path (Windows)
python.cli.path=C:\\Users\\user\\chatbot\\backend-python-cli\\chatbot_cli.py
```

## Development

### Project Structure

```
orchestrator-java/
├── src/
│   └── main/
│       ├── java/com/chatbot/orchestrator/
│       │   ├── OrchestratorApplication.java  # Main application
│       │   ├── controller/
│       │   │   └── ChatController.java       # REST endpoints
│       │   ├── service/
│       │   │   └── ChatService.java          # CLI integration
│       │   └── model/
│       │       ├── MessageRequest.java       # Request DTO
│       │       └── MessageResponse.java      # Response DTO
│       └── resources/
│           └── application.properties        # Configuration
├── logs/                                     # Transaction logs
├── pom.xml                                   # Maven configuration
└── README.md                                 # This file
```

### Technologies Used

- **Spring Boot 3.2**: Web framework
- **Java 17**: Language version
- **Jackson**: JSON processing
- **Lombok**: Reduce boilerplate code
- **ProcessBuilder**: Execute Python CLI
- **Maven**: Build and dependency management

## Differences from Flask Version

| Feature | Flask Version | CLI Version |
|---------|--------------|-------------|
| Python Communication | HTTP REST API (RestTemplate) | Process execution (ProcessBuilder) |
| Python Port | 5000 | N/A |
| Response Format | HTTP Response | stdout JSON |
| Error Handling | HTTP status codes | Process exit codes + JSON |
| Dependencies | RestTemplate | ProcessBuilder (built-in) |

## Testing

### Manual Testing

1. Start the orchestrator:
```bash
mvn spring-boot:run
```

2. Test health endpoint:
```bash
curl http://localhost:8080/api/health
```

3. Test message endpoint:
```bash
curl -X POST http://localhost:8080/api/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Test message"}'
```

### Integration Testing

Ensure all three components work together:

1. Start Java orchestrator (port 8080)
2. Start React frontend (port 3000)
3. Open browser to http://localhost:3000
4. Send a message and verify response

## Troubleshooting

### Python CLI not found

Error: `Cannot run program "python"`

**Solution:** Verify Python is in PATH or set full path:
```properties
python.executable=C:\\Python311\\python.exe
```

### CLI script not found

Error: `python: can't open file 'chatbot_cli.py'`

**Solution:** Verify the path in `application.properties`:
```bash
# Check if file exists
ls ../backend-python-cli/chatbot_cli.py
```

### Process timeout

Error: `Python CLI process timed out`

**Solution:** The CLI has a 10-second timeout. Check:
- Python CLI is working correctly
- No infinite loops in CLI code
- Increase timeout in `ChatService.java` if needed

### Empty response

Error: `Python CLI returned empty response`

**Solution:**
- Check CLI stdout is writing JSON
- Verify CLI doesn't have errors (check stderr)
- Run CLI manually to test: `python chatbot_cli.py -m "test"`

### Port already in use

Error: `Port 8080 is already in use`

**Solution:** Change port in `application.properties`:
```properties
server.port=8081
```

Don't forget to update React frontend to use the new port!

## Performance Considerations

- **Process overhead**: Each request spawns a new Python process
- **Startup time**: Python interpreter startup adds latency (~100-500ms)
- **Concurrency**: Multiple requests spawn multiple processes
- **Timeout**: 10-second timeout prevents hanging processes

For production, consider:
- Keep Python CLI process running and communicate via pipes/sockets
- Use a process pool
- Implement caching for repeated requests
- Monitor process creation and resource usage

## Future Enhancements

Possible improvements:
- Persistent Python CLI process (reduce startup overhead)
- Request queuing and rate limiting
- Metrics and monitoring
- Circuit breaker pattern for CLI failures
- Async processing with WebSockets
- Database for transaction logs
