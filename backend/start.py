#!/usr/bin/env python3
"""
Start script for Smart Travel Planner Backend
"""

import os
import sys
import uvicorn
from pathlib import Path

def main():
    """Start the FastAPI server"""
    
    # Add the backend directory to Python path
    backend_dir = Path(__file__).parent
    sys.path.insert(0, str(backend_dir))
    
    # Check if .env file exists
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("⚠️  Warning: .env file not found!")
        print("📝 Please copy env.example to .env and add your API keys")
        print("   cp env.example .env")
        print()
    
    # Get configuration from environment
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 8000))
    
    print("🚀 Starting Smart Travel Planner Backend...")
    print(f"📍 Server will be available at: http://{host}:{port}")
    print("🛑 Press Ctrl+C to stop the server")
    print()
    
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
