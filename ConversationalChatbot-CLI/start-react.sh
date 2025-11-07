#!/bin/bash
echo "============================================"
echo "Starting React Frontend on Port 3000"
echo "============================================"
cd frontend-react

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo "Starting React development server..."
npm start
