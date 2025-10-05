@echo off
REM Smart Travel Planner Startup Script for Windows

echo 🌟 Starting Smart Travel Planner...
echo ==================================

REM Check if we're in the right directory
if not exist "backend" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check prerequisites
echo 🔍 Checking prerequisites...

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is required but not installed
    pause
    exit /b 1
)

npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is required but not installed
    pause
    exit /b 1
)

echo ✅ All prerequisites found

REM Start backend
echo.
echo 🚀 Starting backend server...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing Python dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found!
    echo 📝 Please copy env.example to .env and add your API keys:
    echo    copy env.example .env
    echo.
)

REM Start backend in background
echo 🌐 Starting FastAPI server on http://localhost:8000
start /b python start.py

REM Go back to root and start frontend
cd ..\frontend

echo.
echo 🎨 Starting frontend server...

REM Install dependencies
echo 📥 Installing Node.js dependencies...
npm install

REM Start frontend
echo 🌐 Starting React app on http://localhost:3000
start /b npm run dev

echo.
echo 🎉 Smart Travel Planner is starting up!
echo 📍 Frontend: http://localhost:3000
echo 📍 Backend API: http://localhost:8000
echo 📍 API Docs: http://localhost:8000/docs
echo.
echo 🛑 Press any key to stop both servers

pause >nul

echo.
echo 🛑 Stopping servers...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
echo 👋 Goodbye!
