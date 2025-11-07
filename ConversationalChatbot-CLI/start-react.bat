@echo off
echo ============================================
echo Starting React Frontend on Port 3000
echo ============================================
cd frontend-react

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Installing dependencies...
    call npm install
)

echo Starting React development server...
call npm start
