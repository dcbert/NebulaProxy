"""Routes for proxying requests to target applications"""
import httpx
from fastapi import APIRouter, HTTPException, Request, Response

from ..services.proxy_service import ProxyService
from ..utils.headers import modify_headers_for_proxy, modify_response_headers
from ..utils.rewrite import rewrite_css_content, rewrite_html_content

router = APIRouter(prefix="/proxy", tags=["proxy"])


@router.api_route("/{proxy_id}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_request(proxy_id: str, path: str, request: Request):
    """Proxy requests to target URLs"""
    proxy_config = ProxyService.get_proxy_by_id(proxy_id)

    if not proxy_config:
        raise HTTPException(status_code=404, detail="Proxy not found")

    if not proxy_config.get('enabled', True):
        raise HTTPException(status_code=403, detail="Proxy is disabled")

    target_url = proxy_config['target_url'].rstrip('/')
    full_url = f"{target_url}/{path}"

    # Add query parameters
    if request.url.query:
        full_url = f"{full_url}?{request.url.query}"

    # Prepare headers
    headers = modify_headers_for_proxy(dict(request.headers), target_url, proxy_id)

    # Get request body if present
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            response = await client.request(
                method=request.method,
                url=full_url,
                headers=headers,
                content=body,
            )

            # Check if content is HTML and rewrite it
            content_type = response.headers.get('content-type', '')
            if 'text/html' in content_type:
                content = response.text
                content = rewrite_html_content(content, proxy_id, target_url)
                # Remove encoding headers since we decoded the content
                response_headers = modify_response_headers(dict(response.headers), remove_encoding=True)
                return Response(
                    content=content,
                    status_code=response.status_code,
                    headers=response_headers,
                    media_type="text/html"
                )

            # Check if content is CSS and rewrite it
            if 'text/css' in content_type or path.endswith('.css'):
                content = response.text
                content = rewrite_css_content(content, proxy_id)
                # Remove encoding headers since we decoded the content
                response_headers = modify_response_headers(dict(response.headers), remove_encoding=True)
                return Response(
                    content=content,
                    status_code=response.status_code,
                    headers=response_headers,
                    media_type="text/css"
                )

            # For other content types, pass through as-is with standard header modifications
            response_headers = modify_response_headers(dict(response.headers))

            # For other content types, return as-is
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=response_headers,
                media_type=content_type
            )

    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Error connecting to target: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proxy error: {str(e)}")
