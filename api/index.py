import sys
import os

# Add project root to Python search path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.server.main import app as fastapi_app


class VercelPathNormalizer:
    """
    ASGI middleware that ensures endpoints resolve properly regardless of how
    Vercel strips or preserves the '/api' prefix in serverless routing.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] in ("http", "websocket"):
            path = scope.get("path", "")
            if path.startswith("/v1/"):
                scope["path"] = f"/api{path}"
            elif path.startswith("/api/api/"):
                scope["path"] = path[4:]
        await self.app(scope, receive, send)


app = VercelPathNormalizer(fastapi_app)

