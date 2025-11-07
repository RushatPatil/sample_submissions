#!/bin/bash
echo "============================================"
echo "Testing Python CLI Backend"
echo "============================================"
cd backend-python-cli

echo ""
echo "Test 1: Health Check"
echo "------------------------------------"
python3 chatbot_cli.py --health

echo ""
echo "Test 2: Single Message"
echo "------------------------------------"
python3 chatbot_cli.py -m "Hello from test script"

echo ""
echo "Test 3: Check Output Directory"
echo "------------------------------------"
if [ -d "output" ]; then
    echo "Output directory exists"
    ls -l output/*.json
else
    echo "Output directory not found!"
fi

echo ""
echo "============================================"
echo "Tests Complete!"
echo "============================================"
