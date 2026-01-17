import os
from pathlib import Path

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = Path("/app/config")
STATIC_DIR = Path("/app/frontend/build/static")
ASSETS_DIR = Path("/app/frontend/build/assets")
FRONTEND_BUILD_DIR = Path("/app/frontend/build")

# Config file
CONFIG_FILE = CONFIG_DIR / "proxies.json"

# Ensure config directory exists
CONFIG_DIR.mkdir(exist_ok=True)

# CORS settings
CORS_ORIGINS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Static file extensions
ALLOWED_STATIC_EXTENSIONS = {
    '.js', '.css', '.map', '.jpg', '.jpeg', '.png',
    '.gif', '.svg', '.ico', '.woff', '.woff2',
    '.ttf', '.eot', '.json', '.webp'
}
