"""MDN documentation URLs for standard HTTP headers.

This module provides a mapping of HTTP header names (case-insensitive) to their
MDN documentation URLs. It covers both request and response headers.
"""

MDN_BASE_URL = "https://developer.mozilla.org"

# Comprehensive mapping of HTTP headers to their MDN documentation paths.
# Header names are stored in lowercase for case-insensitive lookup.
MDN_HEADER_PATHS: dict[str, str] = {
    # Authentication
    "authorization": "/en-US/docs/Web/HTTP/Headers/Authorization",
    "proxy-authenticate": "/en-US/docs/Web/HTTP/Headers/Proxy-Authenticate",
    "proxy-authorization": "/en-US/docs/Web/HTTP/Headers/Proxy-Authorization",
    "www-authenticate": "/en-US/docs/Web/HTTP/Headers/WWW-Authenticate",
    # Caching
    "age": "/en-US/docs/Web/HTTP/Headers/Age",
    "cache-control": "/en-US/docs/Web/HTTP/Headers/Cache-Control",
    "clear-site-data": "/en-US/docs/Web/HTTP/Headers/Clear-Site-Data",
    "expires": "/en-US/docs/Web/HTTP/Headers/Expires",
    "no-vary-search": "/en-US/docs/Web/HTTP/Headers/No-Vary-Search",
    # Conditionals
    "etag": "/en-US/docs/Web/HTTP/Headers/ETag",
    "if-match": "/en-US/docs/Web/HTTP/Headers/If-Match",
    "if-modified-since": "/en-US/docs/Web/HTTP/Headers/If-Modified-Since",
    "if-none-match": "/en-US/docs/Web/HTTP/Headers/If-None-Match",
    "if-unmodified-since": "/en-US/docs/Web/HTTP/Headers/If-Unmodified-Since",
    "last-modified": "/en-US/docs/Web/HTTP/Headers/Last-Modified",
    "vary": "/en-US/docs/Web/HTTP/Headers/Vary",
    # Connection management
    "connection": "/en-US/docs/Web/HTTP/Headers/Connection",
    "keep-alive": "/en-US/docs/Web/HTTP/Headers/Keep-Alive",
    # Content negotiation
    "accept": "/en-US/docs/Web/HTTP/Headers/Accept",
    "accept-charset": "/en-US/docs/Web/HTTP/Headers/Accept-Charset",
    "accept-encoding": "/en-US/docs/Web/HTTP/Headers/Accept-Encoding",
    "accept-language": "/en-US/docs/Web/HTTP/Headers/Accept-Language",
    "accept-patch": "/en-US/docs/Web/HTTP/Headers/Accept-Patch",
    "accept-post": "/en-US/docs/Web/HTTP/Headers/Accept-Post",
    "accept-ranges": "/en-US/docs/Web/HTTP/Headers/Accept-Ranges",
    # Controls
    "expect": "/en-US/docs/Web/HTTP/Headers/Expect",
    "max-forwards": "/en-US/docs/Web/HTTP/Headers/Max-Forwards",
    # Cookies
    "cookie": "/en-US/docs/Web/HTTP/Headers/Cookie",
    "set-cookie": "/en-US/docs/Web/HTTP/Headers/Set-Cookie",
    # CORS
    "access-control-allow-credentials": "/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Credentials",
    "access-control-allow-headers": "/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers",
    "access-control-allow-methods": "/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Methods",
    "access-control-allow-origin": "/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin",
    "access-control-expose-headers": "/en-US/docs/Web/HTTP/Headers/Access-Control-Expose-Headers",
    "access-control-max-age": "/en-US/docs/Web/HTTP/Headers/Access-Control-Max-Age",
    "access-control-request-headers": "/en-US/docs/Web/HTTP/Headers/Access-Control-Request-Headers",
    "access-control-request-method": "/en-US/docs/Web/HTTP/Headers/Access-Control-Request-Method",
    "origin": "/en-US/docs/Web/HTTP/Headers/Origin",
    "timing-allow-origin": "/en-US/docs/Web/HTTP/Headers/Timing-Allow-Origin",
    # Downloads
    "content-disposition": "/en-US/docs/Web/HTTP/Headers/Content-Disposition",
    # Message body information
    "content-encoding": "/en-US/docs/Web/HTTP/Headers/Content-Encoding",
    "content-language": "/en-US/docs/Web/HTTP/Headers/Content-Language",
    "content-length": "/en-US/docs/Web/HTTP/Headers/Content-Length",
    "content-location": "/en-US/docs/Web/HTTP/Headers/Content-Location",
    "content-range": "/en-US/docs/Web/HTTP/Headers/Content-Range",
    "content-type": "/en-US/docs/Web/HTTP/Headers/Content-Type",
    # Proxies
    "forwarded": "/en-US/docs/Web/HTTP/Headers/Forwarded",
    "via": "/en-US/docs/Web/HTTP/Headers/Via",
    # Redirects
    "location": "/en-US/docs/Web/HTTP/Headers/Location",
    "refresh": "/en-US/docs/Web/HTTP/Headers/Refresh",
    # Request context
    "from": "/en-US/docs/Web/HTTP/Headers/From",
    "host": "/en-US/docs/Web/HTTP/Headers/Host",
    "referer": "/en-US/docs/Web/HTTP/Headers/Referer",
    "referrer-policy": "/en-US/docs/Web/HTTP/Headers/Referrer-Policy",
    "user-agent": "/en-US/docs/Web/HTTP/Headers/User-Agent",
    # Response context
    "allow": "/en-US/docs/Web/HTTP/Headers/Allow",
    "server": "/en-US/docs/Web/HTTP/Headers/Server",
    # Range requests
    "if-range": "/en-US/docs/Web/HTTP/Headers/If-Range",
    "range": "/en-US/docs/Web/HTTP/Headers/Range",
    # Security
    "content-security-policy": "/en-US/docs/Web/HTTP/Headers/Content-Security-Policy",
    "content-security-policy-report-only": "/en-US/docs/Web/HTTP/Headers/Content-Security-Policy-Report-Only",
    "cross-origin-embedder-policy": "/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy",
    "cross-origin-opener-policy": "/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy",
    "cross-origin-resource-policy": "/en-US/docs/Web/HTTP/Headers/Cross-Origin-Resource-Policy",
    "expect-ct": "/en-US/docs/Web/HTTP/Headers/Expect-CT",
    "permissions-policy": "/en-US/docs/Web/HTTP/Headers/Permissions-Policy",
    "strict-transport-security": "/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security",
    "upgrade-insecure-requests": "/en-US/docs/Web/HTTP/Headers/Upgrade-Insecure-Requests",
    "x-content-type-options": "/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options",
    "x-frame-options": "/en-US/docs/Web/HTTP/Headers/X-Frame-Options",
    "x-xss-protection": "/en-US/docs/Web/HTTP/Headers/X-XSS-Protection",
    # Fetch metadata
    "sec-fetch-dest": "/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Dest",
    "sec-fetch-mode": "/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Mode",
    "sec-fetch-site": "/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Site",
    "sec-fetch-user": "/en-US/docs/Web/HTTP/Headers/Sec-Fetch-User",
    "sec-purpose": "/en-US/docs/Web/HTTP/Headers/Sec-Purpose",
    "service-worker-navigation-preload": "/en-US/docs/Web/HTTP/Headers/Service-Worker-Navigation-Preload",
    # Server-sent events
    "report-to": "/en-US/docs/Web/HTTP/Headers/Report-To",
    # Transfer coding
    "te": "/en-US/docs/Web/HTTP/Headers/TE",
    "trailer": "/en-US/docs/Web/HTTP/Headers/Trailer",
    "transfer-encoding": "/en-US/docs/Web/HTTP/Headers/Transfer-Encoding",
    # WebSockets
    "sec-websocket-accept": "/en-US/docs/Web/HTTP/Headers/Sec-WebSocket-Accept",
    "sec-websocket-extensions": "/en-US/docs/Web/HTTP/Headers/Sec-WebSocket-Extensions",
    "sec-websocket-key": "/en-US/docs/Web/HTTP/Headers/Sec-WebSocket-Key",
    "sec-websocket-protocol": "/en-US/docs/Web/HTTP/Headers/Sec-WebSocket-Protocol",
    "sec-websocket-version": "/en-US/docs/Web/HTTP/Headers/Sec-WebSocket-Version",
    # Other
    "alt-svc": "/en-US/docs/Web/HTTP/Headers/Alt-Svc",
    "alt-used": "/en-US/docs/Web/HTTP/Headers/Alt-Used",
    "date": "/en-US/docs/Web/HTTP/Headers/Date",
    "link": "/en-US/docs/Web/HTTP/Headers/Link",
    "retry-after": "/en-US/docs/Web/HTTP/Headers/Retry-After",
    "server-timing": "/en-US/docs/Web/HTTP/Headers/Server-Timing",
    "sourcemap": "/en-US/docs/Web/HTTP/Headers/SourceMap",
    "upgrade": "/en-US/docs/Web/HTTP/Headers/Upgrade",
    # Privacy
    "dnt": "/en-US/docs/Web/HTTP/Headers/DNT",
    "sec-gpc": "/en-US/docs/Web/HTTP/Headers/Sec-GPC",
    # Deprecated
    "pragma": "/en-US/docs/Web/HTTP/Headers/Pragma",
    "warning": "/en-US/docs/Web/HTTP/Headers/Warning",
    # Non-standard but widely used
    "x-forwarded-for": "/en-US/docs/Web/HTTP/Headers/X-Forwarded-For",
    "x-forwarded-host": "/en-US/docs/Web/HTTP/Headers/X-Forwarded-Host",
    "x-forwarded-proto": "/en-US/docs/Web/HTTP/Headers/X-Forwarded-Proto",
    # Experimental
    "accept-push-policy": "/en-US/docs/Web/HTTP/Headers/Accept-Push-Policy",
    "accept-signature": "/en-US/docs/Web/HTTP/Headers/Accept-Signature",
    "early-data": "/en-US/docs/Web/HTTP/Headers/Early-Data",
    "origin-isolation": "/en-US/docs/Web/HTTP/Headers/Origin-Isolation",
    "signature": "/en-US/docs/Web/HTTP/Headers/Signature",
    "signed-headers": "/en-US/docs/Web/HTTP/Headers/Signed-Headers",
}


def get_mdn_url(header_name: str) -> str | None:
    """Get the MDN documentation URL for a given HTTP header.

    Args:
        header_name: The HTTP header name (case-insensitive).

    Returns:
        The full MDN URL if the header has documentation, None otherwise.
    """
    path = MDN_HEADER_PATHS.get(header_name.lower())
    if path:
        return f"{MDN_BASE_URL}{path}"
    return None


def has_mdn_docs(header_name: str) -> bool:
    """Check if an HTTP header has MDN documentation.

    Args:
        header_name: The HTTP header name (case-insensitive).

    Returns:
        True if the header has MDN documentation, False otherwise.
    """
    return header_name.lower() in MDN_HEADER_PATHS
