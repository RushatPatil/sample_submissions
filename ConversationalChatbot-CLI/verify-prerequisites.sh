#!/bin/bash

echo "============================================"
echo "Verifying Prerequisites"
echo "============================================"
echo ""

ALL_OK=1

echo "Checking Python..."
if command -v python3 &> /dev/null; then
    python3 --version
    echo "[OK] Python is installed"
elif command -v python &> /dev/null; then
    python --version
    echo "[OK] Python is installed"
else
    echo "[FAIL] Python is not installed or not in PATH"
    ALL_OK=0
fi
echo ""

echo "Checking Java..."
if command -v java &> /dev/null; then
    java -version 2>&1 | head -n 1
    echo "[OK] Java is installed"
else
    echo "[FAIL] Java is not installed or not in PATH"
    ALL_OK=0
fi
echo ""

echo "Checking Maven..."
if command -v mvn &> /dev/null; then
    mvn --version | head -n 1
    echo "[OK] Maven is installed"
else
    echo "[FAIL] Maven is not installed or not in PATH"
    ALL_OK=0
fi
echo ""

echo "Checking Node.js..."
if command -v node &> /dev/null; then
    node --version
    echo "[OK] Node.js is installed"
else
    echo "[FAIL] Node.js is not installed or not in PATH"
    ALL_OK=0
fi
echo ""

echo "Checking npm..."
if command -v npm &> /dev/null; then
    npm --version
    echo "[OK] npm is installed"
else
    echo "[FAIL] npm is not installed or not in PATH"
    ALL_OK=0
fi
echo ""

echo "============================================"
if [ $ALL_OK -eq 1 ]; then
    echo "[SUCCESS] All prerequisites are installed!"
    echo "You can now run the application."
else
    echo "[ERROR] Some prerequisites are missing."
    echo "Please install the missing tools and try again."
fi
echo "============================================"
