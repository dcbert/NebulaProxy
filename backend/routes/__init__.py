"""Routes module initialization"""
from .proxy_handler import router as proxy_handler_router
from .proxy_routes import router as proxy_routes_router
from .static_routes import router as static_routes_router

__all__ = ['proxy_routes_router', 'proxy_handler_router', 'static_routes_router']
