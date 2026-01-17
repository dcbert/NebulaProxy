from typing import Optional

from pydantic import BaseModel


class ProxyConfig(BaseModel):
    """Proxy configuration model"""
    id: str
    name: str
    target_url: str
    description: Optional[str] = ""
    enabled: bool = True


class ProxyCreate(BaseModel):
    """Model for creating a new proxy"""
    name: str
    target_url: str
    description: Optional[str] = ""
    enabled: bool = True
    id: Optional[str] = None


class ProxyUpdate(BaseModel):
    """Model for updating an existing proxy"""
    name: Optional[str] = None
    target_url: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
