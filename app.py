#!/usr/bin/env python3
"""
Hugging Face Spaces entry point for LLM Code Deployment API
"""

import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

# Hugging Face Spaces will automatically detect this FastAPI app
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))  # Hugging Face uses port 7860
    uvicorn.run(app, host="0.0.0.0", port=port)
