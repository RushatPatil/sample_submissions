# ConversationalChatbot

A complete multi-component chatbot system demonstrating microservices architecture with React frontend, Java Spring Boot orchestrator, and Python Flask backend.

## Project Structure

```
ConversationalChatbot/
│
├── frontend-react/          # React-based UI (Port 3000)
│   ├── src/
│   │   ├── App.js          # Main chat component
│   │   ├── App.css         # Styling
│   │   ├── index.js        # Entry point
│   │   └── index.css
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── README.md
│
├── orchestrator-java/       # Java Spring Boot orchestrator (Port 8080)
│   ├── src/
│   │   └── main/
│   │       ├── java/com/chatbot/orchestrator/
│   │       │   ├── OrchestratorApplication.java
│   │       │   ├── controller/
│   │       │   │   └── ChatController.java
│   │       │   ├── service/
│   │       │   │   └── ChatService.java
│   │       │   └── model/
│   │       │       ├── MessageRequest.java
│   │       │       ├── MessageResponse.java
│   │       │       ├── PythonRequest.java
│   │       │       └── PythonResponse.java
│   │       └── resources/
│   │           └── application.properties
│   ├── logs/               # Transaction logs
│   ├── pom.xml
│   └── README.md
│
└── backend-python/          # Python Flask backend (Port 5000)
    ├── app.py              # Flask application
    ├── requirements.txt    # Python dependencies
    ├── output/             # Conversation logs
    └── README.md
```

## System Architecture

```
┌─────────────────┐
│  React Frontend │  (Port 3000)
│   User Interface│
└────────┬────────┘
         │ HTTP POST /api/message
         │ { "message": "..." }
         ▼
┌─────────────────┐
│ Java Orchestrator│ (Port 8080)
│  Spring Boot    │
└────────┬────────┘
         │ HTTP POST /chat
         │ { "user_message": "..." }
         ▼
┌─────────────────┐
│ Python Backend  │  (Port 5000)
│   Flask API     │
│  + Conversation  │
│     Logging      │
└─────────────────┘
```

## Features

- **React Frontend**: Modern, responsive chat UI with real-time updates
- **Java Orchestrator**: Middleware service for routing and transaction logging
- **Python Backend**: Message processing and conversation storage
- **Conversation Logging**: All chats saved to JSON files with timestamps
- **Error Handling**: Comprehensive error messages and logging
- **Health Checks**: Each service has health check endpoints

## Prerequisites

Make sure you have the following installed:

- **Node.js** 14+ and npm (for React frontend)
- **Java** 17+ and Maven 3.6+ (for Java orchestrator)
- **Python** 3.8+ and pip (for Python backend)

### Verify installations:

```bash
node --version
npm --version
java -version
mvn -version
python --version
pip --version
```

## Quick Start

### 1. Start the Python Backend (Port 5000)

```bash
cd backend-python

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The backend will start on `http://localhost:5000`

### 2. Start the Java Orchestrator (Port 8080)

Open a new terminal:

```bash
cd orchestrator-java

# Run with Maven
mvn spring-boot:run

# OR build and run the JAR
# mvn clean package
# java -jar target/orchestrator-1.0.0.jar
```

The orchestrator will start on `http://localhost:8080`

### 3. Start the React Frontend (Port 3000)

Open another new terminal:

```bash
cd frontend-react

# Install dependencies
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

## API Flow Example

**User types:** "Hello chatbot"

1. **React Frontend** → POST to `http://localhost:8080/api/message`
   ```json
   { "message": "Hello chatbot" }
   ```

2. **Java Orchestrator** → POST to `http://localhost:5000/chat`
   ```json
   { "user_message": "Hello chatbot" }
   ```

3. **Python Backend** → Processes and responds:
   ```json
   { "assistant_response": "I listened to you: Hello chatbot" }
   ```

4. **Java Orchestrator** → Returns to React:
   ```json
   { "response": "I listened to you: Hello chatbot" }
   ```

5. **React Frontend** → Displays the message in the chat window

6. **Python Backend** → Saves conversation to:
   ```
   backend-python/output/session_<timestamp>.json
   ```

## Logging and Output

### Python Backend
- Conversations saved to: `backend-python/output/session_YYYYMMDD_HHMMSS.json`
- Console logs show all requests and responses

### Java Orchestrator
- Transaction logs: `orchestrator-java/logs/orchestrator.log`
- Contains timestamps, request/response details

### React Frontend
- Browser console shows API calls and responses
- Error messages displayed in UI

## Health Checks

Each service provides a health check endpoint:

- **React**: Open `http://localhost:3000` (visual check)
- **Java**: GET `http://localhost:8080/api/health`
- **Python**: GET `http://localhost:5000/health`

## Troubleshooting

### Connection Errors

If the frontend shows connection errors:
1. Verify all three services are running
2. Check the ports: 3000 (React), 8080 (Java), 5000 (Python)
3. Ensure no firewalls are blocking the connections

### Python Backend Not Starting

- Check if port 5000 is already in use
- Verify Flask is installed: `pip list | grep Flask`
- Check Python version: `python --version`

### Java Orchestrator Not Starting

- Verify Java 17+ is installed
- Check if port 8080 is already in use
- Ensure Maven dependencies are downloaded: `mvn dependency:resolve`

### React Not Starting

- Delete `node_modules` and run `npm install` again
- Clear npm cache: `npm cache clean --force`
- Check if port 3000 is already in use

## Stopping the Services

Press `Ctrl+C` in each terminal to stop the respective service.

## Project Highlights

- **No AI/LLM Dependencies**: Pure string manipulation logic
- **Microservices Architecture**: Three independent, loosely-coupled components
- **RESTful APIs**: Standard HTTP JSON communication
- **Self-Contained**: All code and configs included
- **Comprehensive Logging**: Full audit trail of all conversations
- **Modern Stack**: React 18, Spring Boot 3, Flask 3

## Future Enhancements

Potential improvements:
- Add authentication and user sessions
- Implement WebSocket for real-time updates
- Add database for conversation persistence
- Deploy using Docker containers
- Add unit and integration tests
- Implement rate limiting
- Add message history retrieval

## License

This is a demonstration project for educational purposes.

## Contributing

This is a standalone demo project. Feel free to fork and modify for your needs.

---

**Created**: 2025
**Tech Stack**: React, Java Spring Boot, Python Flask
