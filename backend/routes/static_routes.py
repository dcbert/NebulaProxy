"""Routes for serving React frontend static files"""
import mimetypes
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

from ..config.settings import ALLOWED_STATIC_EXTENSIONS

router = APIRouter(tags=["frontend"])


@router.get("/", response_class=HTMLResponse)
async def serve_root():
    """Serve the React frontend at root"""
    frontend_path = Path("/app/frontend/build/index.html")
    if frontend_path.exists():
        return HTMLResponse(frontend_path.read_text())
    return HTMLResponse(
        "<h1>Frontend not built yet</h1>"
        "<p>Run: cd frontend && npm install && npm run build</p>"
    )


@router.get("/{file_path:path}")
async def serve_frontend_files(file_path: str):
    """Serve React frontend static files only"""
    # Skip internal routes
    if file_path.startswith("_rproxy/") or file_path.startswith("proxy/"):
        raise HTTPException(status_code=404)

    # Only serve static assets (js, css, fonts, images, etc.)
    # This prevents serving index.html for arbitrary paths
    file_full_path = Path("/app/frontend/build") / file_path

    # Check if file exists and has an allowed extension
    if file_full_path.exists() and file_full_path.is_file():
        file_ext = file_full_path.suffix.lower()
        if file_ext in ALLOWED_STATIC_EXTENSIONS:
            # Guess mime type
            mime_type, _ = mimetypes.guess_type(str(file_full_path))
            if mime_type:
                return FileResponse(file_full_path, media_type=mime_type)
            return FileResponse(file_full_path)

    # Return 404 for everything else
    raise HTTPException(status_code=404)
