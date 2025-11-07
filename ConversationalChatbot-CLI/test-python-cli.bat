@echo off
echo ============================================
echo Testing Python CLI Backend
echo ============================================
cd backend-python-cli

echo.
echo Test 1: Health Check
echo ------------------------------------
python chatbot_cli.py --health

echo.
echo Test 2: Single Message
echo ------------------------------------
python chatbot_cli.py -m "Hello from test script"

echo.
echo Test 3: Check Output Directory
echo ------------------------------------
if exist "output\" (
    echo Output directory exists
    dir /b output\*.json
) else (
    echo Output directory not found!
)

echo.
echo ============================================
echo Tests Complete!
echo ============================================
pause
