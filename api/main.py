"""
FastAPI application entry point
Main API server for Document Verification System
"""

from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from pathlib import Path
import sys
from config import get_settings
from api.routes import verification
from api.middleware import APITokenMiddleware, get_swagger_login_page

# Get settings
settings = get_settings()


def validate_required_settings():
    """
    Validate that all required environment variables are set at startup.
    This provides clear error messages before the server starts.
    """
    errors = []
    
    # Required settings
    if not settings.github_token:
        errors.append("GITHUB_TOKEN is required but not set in environment variables")
    
    # Note: BEARER_TOKEN is optional - if not set, API protection is disabled
    # This is intentional for backward compatibility
    
    # Celery settings validation
    if not settings.celery_broker_url:
        errors.append("CELERY_BROKER_URL is required but not set in environment variables")
    
    if not settings.celery_result_backend:
        errors.append("CELERY_RESULT_BACKEND is required but not set in environment variables")
    
    # Webhook validation (only if enabled)
    if settings.webhook_enable:
        if not settings.webhook_url:
            errors.append("WEBHOOK_URL is required when WEBHOOK_ENABLE=true but not set")
        if not settings.webhook_token:
            errors.append("WEBHOOK_TOKEN is required when WEBHOOK_ENABLE=true but not set")
    
    if errors:
        error_message = "\n".join([f"  ❌ {error}" for error in errors])
        print("\n" + "=" * 60, file=sys.stderr)
        print("🚨 STARTUP VALIDATION FAILED", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print("Missing required environment variables:\n", file=sys.stderr)
        print(error_message, file=sys.stderr)
        print("\nPlease set these variables in your .env file or environment.", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)
        sys.exit(1)
    
    # Success message (only in development/debug mode)
    print("✅ Startup validation passed - all required settings are configured")


# Validate settings at startup
validate_required_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="""
    Document Verification API.
    
    This API verifies documents by:
    1. Processing documents through Stark's AI System
    2. Calculating accuracy by comparing with actual data
    3. Returning field-level accuracy results
    
    ## Features
    - Modular architecture
    - Token optimization per document type
    - Swagger documentation
    - Support for multiple services (extensible)
    """,
    docs_url=None,  # Disable default docs - we handle it manually for password protection
    redoc_url="/redoc"
)

# API Token Middleware (protects API endpoints with token)
# Add this FIRST so it runs before CORS (middleware runs in reverse order)
app.add_middleware(APITokenMiddleware)


# CORS middleware (configure as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(verification.router)

# Mount static files for UI (if ui_html directory exists)
ui_path = Path(__file__).parent.parent / "ui_html"
if ui_path.exists():
    # Mount static files FIRST at /ui/static/ so CSS/JS are accessible
    app.mount("/ui/static", StaticFiles(directory=str(ui_path)), name="ui-static")
    
    # Define UI endpoint - serves HTML
    @app.get("/ui", response_class=HTMLResponse, include_in_schema=False)
    @app.get("/ui/", response_class=HTMLResponse, include_in_schema=False)
    async def serve_ui():
        """Serve the main UI page"""
        index_file = ui_path / "index.html"
        if index_file.exists():
            # Read HTML and replace relative paths with /ui/static/ paths
            html_content = index_file.read_text()
            # Replace relative paths with absolute paths
            html_content = html_content.replace('href="styles.css"', 'href="/ui/static/styles.css"')
            html_content = html_content.replace('src="script.js"', 'src="/ui/static/script.js"')
            return HTMLResponse(content=html_content)
        return HTMLResponse(content="<h1>UI not found</h1>", status_code=404)
    
@app.get("/")
async def root(request: Request):
    """Root endpoint - serve UI for browsers, API info for API clients"""
    # If request wants HTML (browser), serve UI
    if ui_path.exists() and "text/html" in request.headers.get("accept", ""):
        index_file = ui_path / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
    # Otherwise return API info (for API clients)
    return {
        "message": "Document Verification API",
        "version": settings.api_version,
        "docs": "/docs",
        "ui": "/ui",
        "health": "/api/v1/health"
    }


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html(request: Request):
    """Protected Swagger UI endpoint - requires password authentication"""
    settings = get_settings()
    
    # If Swagger password is not configured, show Swagger UI directly
    if not settings.swagger_password:
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} - Swagger UI"
        )
    
    # Check if user is authenticated
    session_token = request.cookies.get("swagger_auth")
    if session_token == "authenticated":
        # Authenticated - show Swagger UI
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} - Swagger UI"
        )
    else:
        # Not authenticated - show login page
        return HTMLResponse(content=get_swagger_login_page())


@app.post("/docs", include_in_schema=False)
async def swagger_ui_login(request: Request, password: str = Form(...)):
    """Handle Swagger UI login form submission"""
    settings = get_settings()
    
    # If Swagger password is not configured, redirect to docs
    if not settings.swagger_password:
        return RedirectResponse(url="/docs", status_code=302)
    
    # Validate password
    if password == settings.swagger_password:
        # Authentication successful - set cookie and redirect
        response = RedirectResponse(url="/docs", status_code=302)
        response.set_cookie(
            key="swagger_auth",
            value="authenticated",
            max_age=3600,  # 1 hour
            httponly=True,
            samesite="lax"
        )
        return response
    else:
        # Invalid password - show login page with error
        return HTMLResponse(content=get_swagger_login_page(error="Invalid password. Please try again."))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )

