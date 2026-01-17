"""Utils module initialization"""
from .headers import modify_headers_for_proxy, modify_response_headers
from .rewrite import rewrite_css_content, rewrite_html_content

__all__ = [
    'modify_headers_for_proxy',
    'modify_response_headers',
    'rewrite_html_content',
    'rewrite_css_content'
]
