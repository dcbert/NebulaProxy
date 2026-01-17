"""Utility functions for rewriting HTML, CSS, and JavaScript content"""
import re
from typing import Optional

from bs4 import BeautifulSoup


def rewrite_html_content(content: str, proxy_id: str, target_url: str) -> str:
    """Rewrite HTML content to work through the proxy"""
    try:
        soup = BeautifulSoup(content, 'html.parser')
        proxy_base = f'/proxy/{proxy_id}'

        # Rewrite all absolute URLs in common attributes
        for tag in soup.find_all(['a', 'link', 'script', 'img', 'iframe', 'form', 'video', 'audio', 'source']):
            for attr in ['href', 'src', 'action', 'data', 'poster']:
                if tag.has_attr(attr):
                    url = tag[attr]
                    # Skip if already proxied, empty, or a data/javascript/mailto URL
                    if not url or url.startswith(('data:', 'javascript:', 'mailto:', '#', proxy_base)):
                        continue
                    # Rewrite absolute paths
                    if url.startswith('/'):
                        tag[attr] = f'{proxy_base}{url}'
                    # Rewrite relative URLs (only if they're simple paths without protocols)
                    elif not url.startswith(('http://', 'https://', '//')):
                        tag[attr] = f'{proxy_base}/{url}'

        # Rewrite inline style attributes
        for tag in soup.find_all(style=True):
            original_style = tag['style']
            tag['style'] = rewrite_css_content(original_style, proxy_id)

        # Rewrite <style> blocks
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                original_css = style_tag.string
                rewritten_css = rewrite_css_content(original_css, proxy_id)
                style_tag.string = rewritten_css

        # Inject JavaScript to intercept fetch/XMLHttpRequest
        script = soup.new_tag('script')
        script.string = f"""
        (function() {{
            const proxyBase = '{proxy_base}';
            const targetUrl = '{target_url}';

            // Intercept fetch
            const originalFetch = window.fetch;
            window.fetch = function(url, options) {{
                if (typeof url === 'string' && url.startsWith('/') && !url.startsWith(proxyBase)) {{
                    url = proxyBase + url;
                }}
                return originalFetch(url, options);
            }};

            // Intercept XMLHttpRequest
            const originalOpen = XMLHttpRequest.prototype.open;
            XMLHttpRequest.prototype.open = function(method, url, ...rest) {{
                if (typeof url === 'string' && url.startsWith('/') && !url.startsWith(proxyBase)) {{
                    url = proxyBase + url;
                }}
                return originalOpen.call(this, method, url, ...rest);
            }};
        }})();
        """
        if soup.head:
            soup.head.insert(0, script)
        elif soup.body:
            soup.body.insert(0, script)

        return str(soup)
    except Exception as e:
        # Return original content if rewriting fails
        return content


def rewrite_css_content(content: str, proxy_id: str) -> str:
    """Rewrite CSS content to proxy URL references"""
    try:
        proxy_base = f'/proxy/{proxy_id}'

        def replace_url(match):
            # Extract the URL (remove quotes if present)
            url = match.group(1).strip('\'"').strip()

            # Skip data URIs, already proxied URLs, and hash references
            if url.startswith(('data:', '#', proxy_base)):
                return match.group(0)

            # Skip if already proxied
            if url.startswith(proxy_base):
                return match.group(0)

            # Rewrite absolute paths
            if url.startswith('/'):
                new_url = f'url("{proxy_base}{url}")'
                return new_url
            # Rewrite relative paths
            else:
                new_url = f'url("{proxy_base}/{url}")'
                return new_url

        # Match url(...) with various quote styles
        original_content = content
        content = re.sub(r'url\([\s]*([^)]+)[\s]*\)', replace_url, content)

        return content
    except Exception as e:
        # Return original content if rewriting fails
        return content
