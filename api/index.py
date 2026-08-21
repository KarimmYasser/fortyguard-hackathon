import sys
import os

# Add project root to Python search path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.server.main import app

# Export the FastAPI app for Vercel Serverless Functions
app = app
