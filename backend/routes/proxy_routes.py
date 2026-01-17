"""API routes for proxy management"""
from typing import List

from fastapi import APIRouter, HTTPException, Request

from ..models.proxy import ProxyConfig, ProxyCreate, ProxyUpdate
from ..services.proxy_service import ProxyService

router = APIRouter(prefix="/_rproxy", tags=["proxy-management"])


@router.get("/proxies", response_model=List[ProxyConfig])
async def get_proxies():
    """Get all proxy configurations"""
    return ProxyService.get_all_proxies()


@router.post("/proxies", response_model=ProxyConfig, status_code=201)
async def create_proxy(proxy: ProxyCreate):
    """Create a new proxy configuration"""
    return ProxyService.create_proxy(proxy)


@router.put("/proxies/{proxy_id}", response_model=ProxyConfig)
async def update_proxy(proxy_id: str, proxy: ProxyUpdate):
    """Update a proxy configuration"""
    return ProxyService.update_proxy(proxy_id, proxy)


@router.delete("/proxies/{proxy_id}")
async def delete_proxy(proxy_id: str):
    """Delete a proxy configuration"""
    ProxyService.delete_proxy(proxy_id)
    return {"success": True}
