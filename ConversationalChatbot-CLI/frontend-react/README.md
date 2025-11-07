# React Frontend

This is the React-based frontend for the CLI-based Conversational Chatbot. It provides a modern, responsive chat interface.

## Features

- Modern React 18 UI
- Real-time chat interface
- Message history display
- Loading indicators
- Error handling
- Responsive design
- Auto-scrolling messages

## Requirements

- Node.js 14+
- npm 6+

## Setup

1. Install dependencies:
```bash
cd frontend-react
npm install
```

2. Ensure the Java orchestrator is running on port 8080

## Running the Frontend

```bash
npm start
```

The application will start on `http://localhost:3000` and automatically open in your browser.

## Available Scripts

### `npm start`

Runs the app in development mode.
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.

### `npm run build`

Builds the app for production to the `build` folder.
The build is optimized for best performance.

### `npm test`

Launches the test runner in interactive watch mode.

## Usage

1. Type a message in the input box at the bottom
2. Click "Send" or press Enter
3. The chatbot will respond with your message
4. Continue the conversation
5. Click "Clear Chat" to reset the conversation

## API Integration

The frontend communicates with the Java orchestrator at:
```
http://localhost:8080/api/message
```

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

## Architecture

```
┌─────────────────┐
│  React Frontend │  Port 3000
│   User Browser  │
└────────┬────────┘
         │ HTTP POST /api/message
         │ {"message": "..."}
         ▼
┌─────────────────┐
│ Java Orchestrator│  Port 8080
└────────┬────────┘
         │ ProcessBuilder
         ▼
┌─────────────────┐
│  Python CLI     │
└─────────────────┘
```

## Components

### App.js

Main application component containing:
- `useState` for message state management
- `useEffect` for auto-scrolling
- `sendMessage` function for API calls
- Chat UI rendering

### App.css

Styling for:
- Chat container layout
- Message bubbles (user, assistant, error)
- Input form
- Loading indicators
- Responsive design

## Error Handling

The frontend handles several error scenarios:

1. **Empty message**: Prevents sending empty messages
2. **Network errors**: Displays error message in chat
3. **Server errors**: Shows error with connection details
4. **Timeout**: Browser timeout for slow responses

Error messages are displayed in red within the chat interface.

## Configuration

### Change Backend URL

If the Java orchestrator runs on a different port, update `App.js`:

```javascript
const response = await fetch('http://localhost:8080/api/message', {
  // Change 8080 to your port
```

### CORS

The Java orchestrator has CORS enabled for all origins:
```java
@CrossOrigin(origins = "*")
```

For production, restrict this to your frontend domain.

## Customization

### Styling

Edit `App.css` to customize:
- Colors and themes
- Message bubble styles
- Font sizes
- Layout spacing

### Features

Extend `App.js` to add:
- User authentication
- Message timestamps
- File uploads
- Emoji support
- Markdown rendering

## Project Structure

```
frontend-react/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── App.js              # Main component
│   ├── App.css             # Styling
│   ├── index.js            # Entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies
└── README.md               # This file
```

## Dependencies

- **react**: UI library
- **react-dom**: DOM rendering
- **react-scripts**: Build tooling (Webpack, Babel, etc.)

## Browser Support

Supports all modern browsers:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### Port 3000 already in use

```bash
# Use a different port
PORT=3001 npm start
```

### Cannot connect to backend

Ensure:
1. Java orchestrator is running on port 8080
2. No firewall blocking the connection
3. CORS is enabled on the backend

### npm install fails

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Build errors

```bash
# Update dependencies
npm update

# Or use specific versions
npm install react@18.2.0 react-dom@18.2.0
```

## Production Deployment

1. Build the production bundle:
```bash
npm run build
```

2. Serve the `build` folder with a web server:
```bash
# Using serve
npx serve -s build

# Using nginx, Apache, etc.
```

3. Update backend URL to production server

## Future Enhancements

Possible improvements:
- User authentication
- Message persistence
- WebSocket for real-time updates
- Rich text formatting
- Voice input
- File attachments
- User profiles
- Dark mode
