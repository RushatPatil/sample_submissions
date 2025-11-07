# Java Spring Boot Orchestrator

This is the orchestrator service for the Conversational Chatbot. It acts as a middleware between the React frontend and Python backend.

## Features
- REST API endpoint `/api/message` for receiving messages from frontend
- Forwards requests to Python Flask backend
- Transaction logging to `logs/orchestrator.log`
- Health check endpoint
- CORS enabled for frontend communication

## Prerequisites
- Java 17 or higher
- Maven 3.6+

## Setup

1. Ensure Java and Maven are installed:
```bash
java -version
mvn -version
```

2. Install dependencies (Maven will do this automatically on first run):
```bash
mvn clean install
```

## Running the Service

### Using Maven:
```bash
mvn spring-boot:run
```

### Using Java directly (after building):
```bash
mvn clean package
java -jar target/orchestrator-1.0.0.jar
```

The service will start on `http://localhost:8080`

## API Endpoints

### POST /api/message
Forward a message to the Python backend and return the response.

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

### GET /api/health
Check service health.

**Response:**
```json
{
  "status": "healthy",
  "service": "Java Orchestrator",
  "port": 8080
}
```

## Configuration

Configuration can be modified in `src/main/resources/application.properties`:
- `server.port`: Change the port (default: 8080)
- `python.backend.url`: Python backend URL (default: http://localhost:5000)

## Logs

Transaction logs are stored in `logs/orchestrator.log` with timestamps and message details.

## Architecture

```
React Frontend (port 3000)
        ↓
Java Orchestrator (port 8080) ← You are here
        ↓
Python Backend (port 5000)
```
