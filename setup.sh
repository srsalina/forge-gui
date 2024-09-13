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
echo "Initializing shadcn UI components..."
npx shadcn@latest init

# Step 4: Return to the root directory
cd ..

# Step 5: Build the frontend
echo "Building the frontend..."
npm run build-react

echo "Setup complete! You can now run 'npm run dev' to start the application in development mode."
