#!/usr/bin/env python3
"""
Vercel-compatible entry point for the LLM Code Deployment API
This version processes requests synchronously to work with Vercel's serverless functions
"""

import sys
import os

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.vercel_main import app

# Export the FastAPI app for Vercel
# Vercel will automatically detect this and create a serverless function
handler = app

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
