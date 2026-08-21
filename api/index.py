import sys
import os
import urllib.parse

# Add project root to Python search path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.server.main import app as fastapi_app


class VercelPathNormalizer:
    """
    ASGI middleware that ensures endpoints resolve properly regardless of how
    Vercel strips, preserves, or rewrites the '/api' prefix in serverless routing.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] in ("http", "websocket"):
            raw_path = scope.get("path", "")
            headers_dict = {k.lower(): v for k, v in scope.get("headers", [])}

            # If path was rewritten by Vercel to /api/index.py, /api, or /api/index,
            # inspect Vercel headers to recover the original request path
            if raw_path in ("/api/index.py", "/api/index", "/api", "") or not raw_path.startswith("/api/v1"):
                # 1. Try x-matched-path
                matched = headers_dict.get(b"x-matched-path", b"").decode("utf-8", "ignore")
                if not matched:
                    # 2. Try x-forwarded-uri
                    matched = headers_dict.get(b"x-forwarded-uri", b"").decode("utf-8", "ignore")
                if not matched:
                    # 3. Try x-original-url
                    matched = headers_dict.get(b"x-original-url", b"").decode("utf-8", "ignore")
                if not matched:
                    # 4. Try x-now-route-matches
                    matches = headers_dict.get(b"x-now-route-matches", b"").decode("utf-8", "ignore")
                    if "1=" in matches:
                        for part in matches.split("&"):
                            if part.startswith("1="):
                                matched = urllib.parse.unquote(part[2:])
                                break

                if matched:
                    # Remove query params if attached
                    matched = matched.split("?")[0]
                    # x-now-route-matches values are relative (e.g. "v1/replay/x"),
                    # unlike x-matched-path which is absolute ("/api/v1/replay/x").
                    # Without this, a relative value fell through to the final
                    # else-branch and produced a slashless, unroutable ASGI path.
                    if not matched.startswith("/"):
                        matched = f"/{matched}"
                    if matched.startswith("/v1/"):
                        scope["path"] = f"/api{matched}"
                    elif not matched.startswith("/api"):
                        scope["path"] = f"/api{matched}"
                    else:
                        scope["path"] = matched

            # Re-check current scope path for standard normalizations
            curr_path = scope.get("path", "")
            if curr_path.startswith("/v1/"):
                scope["path"] = f"/api{curr_path}"
            elif curr_path.startswith("/api/api/"):
                scope["path"] = curr_path[4:]

        await self.app(scope, receive, send)


app = VercelPathNormalizer(fastapi_app)


