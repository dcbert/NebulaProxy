"""Utility functions for handling HTTP headers"""
from typing import Dict
from urllib.parse import urlparse


def modify_headers_for_proxy(headers: Dict[str, str], target_url: str, proxy_id: str) -> Dict[str, str]:
    """Modify request headers for proxying"""
    # Remove hop-by-hop headers
    headers_to_remove = ['host', 'connection', 'keep-alive', 'proxy-authenticate',
                          'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade']

    modified_headers = {k: v for k, v in headers.items() if k.lower() not in headers_to_remove}

    # Set proper host header
    parsed = urlparse(target_url)
    modified_headers['host'] = parsed.netloc

    # Update Origin and Referer if present
    if 'origin' in modified_headers:
        modified_headers['origin'] = f"{parsed.scheme}://{parsed.netloc}"

    if 'referer' in modified_headers:
        # Keep the path but update the origin
        original_referer = modified_headers['referer']
        if f'/proxy/{proxy_id}/' in original_referer:
            referer_path = original_referer.split(f'/proxy/{proxy_id}/', 1)[1]
            modified_headers['referer'] = f"{parsed.scheme}://{parsed.netloc}/{referer_path}"

    return modified_headers


def modify_response_headers(headers: Dict[str, str], remove_encoding: bool = False) -> Dict[str, str]:
    """Modify response headers to allow iframe embedding

    Args:
        headers: Original response headers
        remove_encoding: If True, removes content-encoding headers (needed when content is decoded)
    """
    modified_headers = dict(headers)

    # Remove headers that prevent iframe embedding
    headers_to_remove = ['x-frame-options', 'content-security-policy', 'content-security-policy-report-only']
    for header in headers_to_remove:
        modified_headers.pop(header, None)

    # Remove hop-by-hop headers
    hop_by_hop = ['connection', 'keep-alive', 'proxy-authenticate',
                  'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade']
    for header in hop_by_hop:
        modified_headers.pop(header, None)

    # Remove content-encoding if we've decoded the content for rewriting
    if remove_encoding:
        modified_headers.pop('content-encoding', None)
        modified_headers.pop('content-length', None)  # Length will be different after rewriting

    # Add CORS headers
    modified_headers['access-control-allow-origin'] = '*'
    modified_headers['access-control-allow-methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
    modified_headers['access-control-allow-headers'] = '*'

    return modified_headers
