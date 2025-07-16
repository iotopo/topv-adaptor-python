#!/bin/bash
echo "Installing TopV Adaptor Python dependencies..."

echo
echo "Checking Python version..."
python3 --version

echo
echo "Installing required packages..."
pip3 install -r requirements.txt

echo
echo "Making scripts executable..."
chmod +x start.sh
chmod +x test-api.sh

echo
echo "Installation completed!"
echo
echo "To start the service:"
echo "  ./start.sh"
echo
echo "To test the API:"
echo "  ./test-api.sh"
echo 