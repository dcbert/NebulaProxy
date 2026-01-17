"""
Nebula Proxy Web Application
Main application entry point with clean, modular architecture
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config.settings import CORS_ALLOW_CREDENTIALS, CORS_ALLOW_HEADERS, CORS_ALLOW_METHODS, CORS_ORIGINS
from backend.routes import proxy_handler_router, proxy_routes_router, static_routes_router

# Initialize FastAPI application
app = FastAPI(
    title="Nebula Proxy",
    description="Reverse proxy with iframe support for local network applications",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# Mount static files for React app (must be before catch-all routes)
static_dir = Path("/app/frontend/build/static")
assets_dir = Path("/app/frontend/build/assets")

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

# Register route modules
app.include_router(proxy_routes_router)  # Proxy management API routes
app.include_router(proxy_handler_router)  # Proxy request handler
app.include_router(static_routes_router)  # Frontend static file serving


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
