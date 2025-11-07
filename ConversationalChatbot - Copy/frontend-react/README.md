# React Frontend

This is the frontend UI for the Conversational Chatbot built with React.

## Features
- Modern, responsive chat interface
- Real-time message display
- User and assistant message differentiation
- Loading indicators
- Error handling with user-friendly messages
- Auto-scroll to latest messages
- Clear chat functionality

## Prerequisites
- Node.js 14+ and npm

## Setup

1. Install dependencies:
```bash
npm install
```

## Running the Application

```bash
npm start
```

The app will start on `http://localhost:3000` and automatically open in your browser.

## Usage

1. Type your message in the input box at the bottom
2. Click "Send" or press Enter
3. The message is sent to the Java orchestrator at `http://localhost:8080/api/message`
4. The response is displayed in the chat window
5. All conversations are logged by the Python backend

## Features in the UI

- **User Messages**: Displayed on the right in purple
- **Assistant Messages**: Displayed on the left in white
- **Error Messages**: Displayed with red border if there's a connection issue
- **Loading Indicator**: Shows animated dots while waiting for response
- **Clear Chat**: Button in header to clear all messages

## API Integration

The frontend communicates with:
- **Java Orchestrator**: `http://localhost:8080/api/message`

The orchestrator then forwards requests to the Python backend.

## Troubleshooting

If you see connection errors:
1. Ensure the Java orchestrator is running on port 8080
2. Ensure the Python backend is running on port 5000
3. Check that CORS is enabled on both backend services

## Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.
