"""Proxy service for managing proxy configurations"""
import json
from pathlib import Path
from typing import List, Optional

from fastapi import HTTPException

from ..config.settings import CONFIG_FILE
from ..models.proxy import ProxyConfig, ProxyCreate, ProxyUpdate


class ProxyService:
    """Service for managing proxy configurations"""

    @staticmethod
    def load_proxies() -> List[dict]:
        """Load proxy configurations from file"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                # Invalid JSON format, return empty list
                return []
        return []

    @staticmethod
    def save_proxies(proxies: List[dict]) -> None:
        """Save proxy configurations to file"""
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(proxies, f, indent=2)

    @staticmethod
    def get_proxy_by_id(proxy_id: str) -> Optional[dict]:
        """Get a specific proxy configuration by ID"""
        proxies = ProxyService.load_proxies()
        for proxy in proxies:
            if proxy.get('id') == proxy_id:
                return proxy
        return None

    @staticmethod
    def get_all_proxies() -> List[dict]:
        """Get all proxy configurations"""
        return ProxyService.load_proxies()

    @staticmethod
    def create_proxy(proxy_data: ProxyCreate) -> dict:
        """Create a new proxy configuration"""
        proxies = ProxyService.load_proxies()

        # Generate ID from name if not provided
        proxy_dict = proxy_data.model_dump()
        if not proxy_dict.get('id'):
            proxy_dict['id'] = proxy_data.name.lower().replace(' ', '-')

        # Check if ID already exists
        if any(p['id'] == proxy_dict['id'] for p in proxies):
            raise HTTPException(status_code=400, detail="Proxy ID already exists")

        proxies.append(proxy_dict)
        ProxyService.save_proxies(proxies)
        return proxy_dict

    @staticmethod
    def update_proxy(proxy_id: str, proxy_data: ProxyUpdate) -> dict:
        """Update an existing proxy configuration"""
        proxies = ProxyService.load_proxies()

        for i, proxy in enumerate(proxies):
            if proxy['id'] == proxy_id:
                # Update only provided fields
                update_data = proxy_data.model_dump(exclude_unset=True)
                proxies[i] = {**proxy, **update_data, 'id': proxy_id}
                ProxyService.save_proxies(proxies)
                return proxies[i]

        raise HTTPException(status_code=404, detail="Proxy not found")

    @staticmethod
    def delete_proxy(proxy_id: str) -> bool:
        """Delete a proxy configuration"""
        proxies = ProxyService.load_proxies()
        initial_count = len(proxies)
        proxies = [p for p in proxies if p['id'] != proxy_id]

        if len(proxies) == initial_count:
            raise HTTPException(status_code=404, detail="Proxy not found")

        ProxyService.save_proxies(proxies)
        return True
