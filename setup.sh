#!/bin/bash

echo "Setting up the project..."

# Step 1: Install root dependencies (Electron and other main dependencies)
echo "Installing root dependencies..."
npm install

# Step 2: Install frontend dependencies (Vite, React, etc.)
echo "Installing frontend dependencies..."
cd interface-frontend
npm install

# Step 3: Initialize shadcn UI
# echo "Initializing shadcn UI components..."
# npx shadcn@latest init

# Step 4: Return to the root directory
cd ..

# Step 5: Move into the backend directory
echo "Setting up the backend environment..."
cd backend

# Step 6: Create the virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Step 7: Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
# venv\Scripts\activate.bat
# venv\Scripts\Activate.ps1

# Step 8: Installing backend dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

# Step 8: return to root directory
cd ..

echo "Setup complete!"

npm run dev
