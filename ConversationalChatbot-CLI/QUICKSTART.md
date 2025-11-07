# Quick Start Guide

Get the ConversationalChatbot-CLI running in 3 simple steps!

## Prerequisites Check

```bash
# Verify all required tools are installed
python --version   # Should be 3.11+
java -version      # Should be 17+
mvn -version       # Should be 3.6+
node --version     # Should be 14+
npm --version      # Should be 6+
```

## Step 1: Test Python CLI (30 seconds)

```bash
cd backend-python-cli

# Test single message
python chatbot_cli.py -m "Hello"
```

**Expected output:**
```json
{"assistant_response": "I listened to you: Hello"}
```

**If this works, continue to Step 2. If not, troubleshoot Python installation.**

## Step 2: Start Java Orchestrator (1-2 minutes)

Open a **NEW terminal window**:

```bash
cd orchestrator-java

# Start the orchestrator
mvn spring-boot:run
```

**Wait for this message:**
```
==================================================
Java Orchestrator Service Starting...
Port: 8080
Backend: Python CLI
==================================================
```

**Test it:**

In another terminal:
```bash
curl http://localhost:8080/api/health
```

Expected:
```json
{"status":"healthy","service":"Java Orchestrator","port":8080,"backend":"Python CLI"}
```

**Leave this terminal running!**

## Step 3: Start React Frontend (1-2 minutes)

Open a **NEW terminal window**:

```bash
cd frontend-react

# Install dependencies (first time only)
npm install

# Start the frontend
npm start
```

**Your browser will automatically open to http://localhost:3000**

If not, manually open: **http://localhost:3000**

## Test the Complete System

1. In the browser, you should see the chat interface
2. Type: **"Hello chatbot"**
3. Click **Send**
4. You should see: **"I listened to you: Hello chatbot"**

**Success!** All three components are working together.

## What's Happening Behind the Scenes

```
Your Browser (Port 3000)
    ↓ HTTP POST {"message": "Hello chatbot"}
Java Orchestrator (Port 8080)
    ↓ Executes: python chatbot_cli.py -m "Hello chatbot"
Python CLI
    ↓ stdout: {"assistant_response": "I listened to you: Hello chatbot"}
Java Orchestrator
    ↓ Returns: {"response": "I listened to you: Hello chatbot"}
Your Browser
    ↓ Displays: "I listened to you: Hello chatbot"
```

## View Conversation Logs

Check the saved conversations:

```bash
# View Python CLI logs
cat backend-python-cli/output/session_*.json

# View Java orchestrator logs
cat orchestrator-java/logs/orchestrator.log
```

## Stopping Everything

Press `Ctrl+C` in each terminal window:
1. Stop React (terminal 3)
2. Stop Java (terminal 2)
3. Python CLI has no running server to stop

## Common Issues

### Issue: Python CLI returns error

**Solution:** Ensure Python 3.11+ is installed
```bash
python --version
```

### Issue: Java can't find Python CLI

**Error:** `can't open file 'chatbot_cli.py'`

**Solution:** Check path in `orchestrator-java/src/main/resources/application.properties`:
```properties
python.cli.path=../backend-python-cli/chatbot_cli.py
```

Use absolute path if needed:
```properties
python.cli.path=C:/Users/yourname/ConversationalChatbot-CLI/backend-python-cli/chatbot_cli.py
```

### Issue: Port 8080 already in use

**Solution:** Kill the process using port 8080:

Windows:
```bash
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

Linux/Mac:
```bash
lsof -i :8080
kill -9 <PID>
```

### Issue: React can't connect to Java

**Solution:**
1. Verify Java is running: `curl http://localhost:8080/api/health`
2. Check browser console (F12) for errors
3. Ensure CORS is enabled (it should be by default)

### Issue: npm install fails

**Solution:**
```bash
cd frontend-react
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

## Next Steps

1. **Customize the Python CLI**: Edit `backend-python-cli/chatbot_cli.py`
2. **Add Java features**: Edit `orchestrator-java/src/main/java/com/chatbot/orchestrator/service/ChatService.java`
3. **Style the frontend**: Edit `frontend-react/src/App.css`
4. **Read the full docs**: Check `README.md` in each component folder

## Architecture Overview

- **backend-python-cli**: Python 3.11+ CLI app (no dependencies)
- **orchestrator-java**: Java 17 Spring Boot (port 8080)
- **frontend-react**: React 18 UI (port 3000)

## Need Help?

1. Check `README.md` in the project root
2. Check `README.md` in each component folder
3. Review logs:
   - Python: `backend-python-cli/output/*.json`
   - Java: `orchestrator-java/logs/orchestrator.log`
   - React: Browser console (F12)

---

**Enjoy your CLI-based chatbot!**
