@echo off
echo ============================================
echo Verifying Prerequisites
echo ============================================
echo.

set ALL_OK=1

echo Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Python is not installed or not in PATH
    set ALL_OK=0
) else (
    python --version
    echo [OK] Python is installed
)
echo.

echo Checking Java...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Java is not installed or not in PATH
    set ALL_OK=0
) else (
    java -version 2>&1 | findstr /C:"version"
    echo [OK] Java is installed
)
echo.

echo Checking Maven...
mvn --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Maven is not installed or not in PATH
    set ALL_OK=0
) else (
    mvn --version | findstr /C:"Apache Maven"
    echo [OK] Maven is installed
)
echo.

echo Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Node.js is not installed or not in PATH
    set ALL_OK=0
) else (
    node --version
    echo [OK] Node.js is installed
)
echo.

echo Checking npm...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] npm is not installed or not in PATH
    set ALL_OK=0
) else (
    npm --version
    echo [OK] npm is installed
)
echo.

echo ============================================
if %ALL_OK%==1 (
    echo [SUCCESS] All prerequisites are installed!
    echo You can now run the application.
) else (
    echo [ERROR] Some prerequisites are missing.
    echo Please install the missing tools and try again.
)
echo ============================================
pause
