# RUN ME FIRST - Quick Start Instructions

## Step 1: Verify Prerequisites

Run this command to check if you have everything installed:

**Windows:**
```cmd
verify-prerequisites.bat
```

**Linux/Mac:**
```bash
chmod +x verify-prerequisites.sh
./verify-prerequisites.sh
```

### Required Software:
- Python 3.11+
- Java 17+
- Maven 3.6+
- Node.js 14+
- npm 6+

If anything is missing, install it first!

## Step 2: Test Python CLI

**Windows:**
```cmd
test-python-cli.bat
```

**Linux/Mac:**
```bash
chmod +x test-python-cli.sh
./test-python-cli.sh
```

This will verify the Python CLI backend is working correctly.

## Step 3: Start the Services

You need **3 separate terminal windows**.

### Terminal 1: Start Java Orchestrator

**Windows:**
```cmd
start-java.bat
```

**Linux/Mac:**
```bash
chmod +x start-java.sh
./start-java.sh
```

**Wait for:** "Started OrchestratorApplication" message

### Terminal 2: Start React Frontend

**Windows:**
```cmd
start-react.bat
```

**Linux/Mac:**
```bash
chmod +x start-react.sh
./start-react.sh
```

**Wait for:** Browser opens automatically to http://localhost:3000

### Terminal 3: Keep this for monitoring

You can use this terminal to:
- Test the Python CLI manually
- Check logs
- View output files

## Step 4: Test the Application

1. Open browser to: **http://localhost:3000**
2. Type: "Hello chatbot"
3. Click **Send**
4. You should see: "I listened to you: Hello chatbot"

## Troubleshooting

### Python CLI Error
```bash
cd backend-python-cli
python chatbot_cli.py --health
```

### Java Not Starting
- Check if Java 17+ is installed: `java -version`
- Check if port 8080 is free: `netstat -ano | findstr :8080` (Windows)
- View logs in `orchestrator-java/logs/`

### React Not Starting
```bash
cd frontend-react
rm -rf node_modules package-lock.json
npm install
npm start
```

### Connection Error in Browser
1. Verify Java is running: `curl http://localhost:8080/api/health`
2. Check browser console (F12) for errors
3. Ensure no firewall blocking port 8080

## What's Running Where?

- **React Frontend**: http://localhost:3000 (User Interface)
- **Java Orchestrator**: http://localhost:8080 (Middleware)
- **Python CLI**: No port (Executed by Java as needed)

## View Logs

**Python Conversations:**
```
backend-python-cli/output/session_*.json
```

**Java Orchestrator:**
```
orchestrator-java/logs/orchestrator.log
```

**React:**
- Browser Console (F12)

## Stop Everything

Press `Ctrl+C` in each terminal window:
1. Stop React (Terminal 2)
2. Stop Java (Terminal 1)

## Next Steps

- Read `README.md` for detailed documentation
- Read `QUICKSTART.md` for more details
- Read `ARCHITECTURE.md` for technical deep dive
- Check component READMEs in each folder

## Need Help?

1. Run `verify-prerequisites.bat` to check installations
2. Run `test-python-cli.bat` to verify Python works
3. Check logs in each component
4. Read the troubleshooting sections in README.md

---

**Happy Coding!**
