"""
Security middleware for API protection
Handles API token validation
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from config import get_settings


class APITokenMiddleware(BaseHTTPMiddleware):
    """
    Middleware to protect API endpoints with token authentication
    Checks for X-API-Token header and validates against .env token
    Excludes /health endpoint from protection
    """
    
    # Endpoints to exclude from token protection
    EXCLUDED_PATHS = ["/health", "/api/v1/health", "/", "/docs", "/redoc", "/openapi.json"]
    
    async def dispatch(self, request: Request, call_next):
        # Get the path
        path = request.url.path
        
        # Check if path should be excluded (exact match or path starts with excluded + "/")
        # Note: Don't use simple startswith() because "/" would match everything
        is_excluded = False
        for excluded in self.EXCLUDED_PATHS:
            if path == excluded:
                is_excluded = True
                break
            # For paths other than "/", check if path starts with excluded + "/"
            elif excluded != "/" and path.startswith(excluded + "/"):
                is_excluded = True
                break
        
        if is_excluded:
            return await call_next(request)
        
        # Check if it's an API endpoint (starts with /api)
        if path.startswith("/api"):
            settings = get_settings()
            
            # If API token is not configured, skip protection (for backward compatibility)
            if not settings.api_token:
                return await call_next(request)
            
            # Get token from header
            token = request.headers.get("X-API-Token") or request.headers.get("x-api-token")
            
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Missing API token. Please include X-API-Token header.",
                    headers={"WWW-Authenticate": "Token"},
                )
            
            # Validate token
            if token != settings.api_token:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid API token.",
                )
        
        return await call_next(request)


def get_swagger_login_page(error: str = None) -> str:
    """Generate HTML login page for Swagger"""
    error_html = f'<div style="color: red; margin-bottom: 15px; padding: 10px; background: #ffe6e6; border-radius: 5px;">{error}</div>' if error else ""
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Swagger UI - Login Required</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            .login-container {{
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                width: 100%;
                max-width: 400px;
            }}
            h1 {{
                color: #333;
                margin-bottom: 10px;
                text-align: center;
            }}
            .subtitle {{
                color: #666;
                text-align: center;
                margin-bottom: 30px;
                font-size: 14px;
            }}
            form {{
                display: flex;
                flex-direction: column;
            }}
            label {{
                color: #555;
                margin-bottom: 8px;
                font-weight: 500;
            }}
            input[type="password"] {{
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                font-size: 16px;
                margin-bottom: 20px;
                transition: border-color 0.3s;
            }}
            input[type="password"]:focus {{
                outline: none;
                border-color: #667eea;
            }}
            button {{
                padding: 12px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
            }}
            button:hover {{
                transform: translateY(-2px);
            }}
            button:active {{
                transform: translateY(0);
            }}
            .lock-icon {{
                text-align: center;
                font-size: 48px;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="lock-icon">🔒</div>
            <h1>Swagger UI Access</h1>
            <p class="subtitle">Please enter the password to access API documentation</p>
            {error_html}
            <form method="post" action="/docs">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required autofocus>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """
    return html_content

