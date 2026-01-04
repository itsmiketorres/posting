"""
HTTP header definitions and descriptions for tooltips.

This module provides descriptions for standard HTTP headers to help users
understand what each header does. Headers are stored in a dict for O(1) lookups.
"""

# Dictionary mapping lowercase header names to their descriptions.
# Standard headers have descriptions explaining their purpose.
# Headers not in this dict are considered custom/non-standard.
HEADER_DESCRIPTIONS: dict[str, str] = {
    # Authentication
    "authorization": "Credentials for authenticating the client with the server.",
    "proxy-authorization": "Credentials for authenticating the client with a proxy server.",
    "www-authenticate": "Defines the authentication method that should be used to access a resource.",
    "proxy-authenticate": "Defines the authentication method that should be used to access a resource behind a proxy server.",
    # Caching
    "age": "Time in seconds the object has been in a proxy cache.",
    "cache-control": "Directives for caching mechanisms in requests and responses.",
    "clear-site-data": "Clears browsing data (cookies, storage, cache) associated with the requesting website.",
    "expires": "Date/time after which the response is considered stale.",
    "pragma": "Implementation-specific header for backwards compatibility with HTTP/1.0 caches.",
    "warning": "General warning information about possible problems.",
    # Conditionals
    "etag": "A unique identifier for a specific version of a resource.",
    "if-match": "Makes the request conditional; applies the method only if the resource matches the given ETags.",
    "if-none-match": "Makes the request conditional; applies the method only if the resource doesn't match the given ETags.",
    "if-modified-since": "Makes the request conditional; transmits data only if modified after the given date.",
    "if-unmodified-since": "Makes the request conditional; transmits data only if not modified after the given date.",
    "last-modified": "Date and time when the resource was last modified.",
    "vary": "Determines how to match request headers to decide whether a cached response can be used.",
    # Connection management
    "connection": "Controls whether the network connection stays open after the transaction.",
    "keep-alive": "Controls how long a persistent connection should stay open.",
    "upgrade": "Used to upgrade the protocol of the connection.",
    # Content negotiation
    "accept": "Informs the server about the types of data that can be sent back.",
    "accept-charset": "Character encodings the client understands.",
    "accept-encoding": "Encoding algorithms (usually compression) the client understands.",
    "accept-language": "Natural languages and locales preferred by the client.",
    # Controls
    "expect": "Expectations that need to be met by the server to handle the request.",
    "max-forwards": "Maximum number of hops for TRACE method before reflecting back.",
    # Cookies
    "cookie": "HTTP cookies previously sent by the server with Set-Cookie.",
    "set-cookie": "Send cookies from the server to the user agent.",
    # CORS
    "access-control-allow-credentials": "Indicates whether the response can be exposed when credentials flag is true.",
    "access-control-allow-headers": "Headers allowed when making the actual request in CORS.",
    "access-control-allow-methods": "Methods allowed when accessing the resource in CORS.",
    "access-control-allow-origin": "Origins allowed to access the resource in CORS.",
    "access-control-expose-headers": "Headers that can be exposed as part of the response.",
    "access-control-max-age": "How long preflight request results can be cached.",
    "access-control-request-headers": "Headers that will be used when making the actual CORS request.",
    "access-control-request-method": "Method that will be used when making the actual CORS request.",
    "origin": "Indicates where a fetch originates from.",
    "timing-allow-origin": "Origins allowed to see timing resource values.",
    # Downloads
    "content-disposition": "Indicates if content should be displayed inline or as a download attachment.",
    # Message body information
    "content-encoding": "The compression algorithm used on the message body.",
    "content-language": "Natural language(s) intended for the audience.",
    "content-length": "Size of the resource, in bytes.",
    "content-location": "Alternate location for the returned data.",
    "content-range": "Where in a full body message this partial message belongs.",
    "content-type": "The media type of the resource.",
    "transfer-encoding": "The form of encoding used to safely transfer the resource.",
    # Proxies
    "forwarded": "Information from client-facing side of proxy servers.",
    "x-forwarded-for": "Originating IP addresses of a client connecting through a proxy.",
    "x-forwarded-host": "Original host requested by the client.",
    "x-forwarded-proto": "Protocol (HTTP or HTTPS) used by the client.",
    "via": "Added by proxies, showing the proxy chain.",
    # Redirects
    "location": "URL to redirect the page to.",
    "refresh": "Instructs the browser to reload the page or redirect after a delay.",
    # Request context
    "from": "Internet email address for the human user who controls the user agent.",
    "host": "Domain name of the server and port number.",
    "referer": "Address of the previous page that linked to the current one.",
    "referrer-policy": "Controls how much referrer information should be included with requests.",
    "user-agent": "Characteristic string identifying the application and version.",
    # Response context
    "allow": "Valid methods for a specified resource.",
    "server": "Information about the software used by the origin server.",
    # Range requests
    "accept-ranges": "Indicates if the server supports range requests.",
    "range": "The part of a document the server should return.",
    "if-range": "Creates a conditional range request fulfilled only if resource matches.",
    "content-range": "Where in a full body message this partial message belongs.",
    # Security
    "content-security-policy": "Controls resources the browser is allowed to load for a page.",
    "content-security-policy-report-only": "Reports CSP violations without enforcing them.",
    "cross-origin-embedder-policy": "Configures embedding of cross-origin resources.",
    "cross-origin-opener-policy": "Controls sharing of browsing context group with cross-origin documents.",
    "cross-origin-resource-policy": "Prevents other domains from reading the response.",
    "expect-ct": "Allows sites to opt in to certificate transparency requirements.",
    "feature-policy": "Controls which browser features can be used in the current document.",
    "permissions-policy": "Controls which browser features can be used in the current document.",
    "strict-transport-security": "Force communication over HTTPS instead of HTTP.",
    "upgrade-insecure-requests": "Preference for encrypted and authenticated responses.",
    "x-content-type-options": "Prevents browsers from MIME-sniffing a response away from declared content-type.",
    "x-frame-options": "Indicates whether a browser should render the page in a frame.",
    "x-xss-protection": "Enables cross-site scripting filtering.",
    "sec-fetch-dest": "Indicates the destination of the fetch request.",
    "sec-fetch-mode": "Indicates the mode of the fetch request.",
    "sec-fetch-site": "Indicates the relationship between request initiator and resource origin.",
    "sec-fetch-user": "Indicates whether a navigation request was triggered by user activation.",
    # Fetch metadata
    "sec-ch-ua": "Client hint for browser brand and version.",
    "sec-ch-ua-mobile": "Client hint indicating if browser is on a mobile device.",
    "sec-ch-ua-platform": "Client hint for the platform/OS.",
    # Transfer coding
    "te": "Transfer encodings the user agent is willing to accept.",
    "trailer": "Headers that will be present in the trailer part of chunked transfer.",
    # WebSockets
    "sec-websocket-accept": "Server response to the WebSocket handshake.",
    "sec-websocket-extensions": "WebSocket extensions to use.",
    "sec-websocket-key": "Key for WebSocket handshake.",
    "sec-websocket-protocol": "Subprotocols for WebSocket.",
    "sec-websocket-version": "Version of WebSocket protocol.",
    # Other common headers
    "alt-svc": "Alternative services for reaching the website.",
    "alt-used": "Alternative service in use.",
    "date": "Date and time when the message was originated.",
    "link": "Serialized links equivalent to the HTML link element.",
    "retry-after": "How long to wait before making a follow-up request.",
    "service-worker-navigation-preload": "Allows a service worker to request navigation preloads.",
    "sourcemap": "Links to a source map for the generated code.",
    "x-dns-prefetch-control": "Controls DNS prefetching.",
    "x-request-id": "Unique identifier for tracking requests across services.",
    "x-correlation-id": "Identifier for correlating related requests.",
    # Privacy
    "dnt": "User's tracking preference (Do Not Track).",
    "sec-gpc": "User's consent preference for selling/sharing personal information.",
    "tk": "Tracking status that applied to the corresponding request.",
    # Server timing
    "server-timing": "Server-side performance metrics.",
}

# Description shown for headers not in HEADER_DESCRIPTIONS
CUSTOM_HEADER_DESCRIPTION = "Custom header (non-standard)."


def get_header_description(header_name: str) -> str:
    """
    Get the description for a given header name.

    Args:
        header_name: The name of the HTTP header (case-insensitive).

    Returns:
        A description of the header, or the custom header message
        if the header is not a recognized standard header.
    """
    return HEADER_DESCRIPTIONS.get(header_name.lower(), CUSTOM_HEADER_DESCRIPTION)


def is_standard_header(header_name: str) -> bool:
    """
    Check if a header is a recognized standard header.

    Args:
        header_name: The name of the HTTP header (case-insensitive).

    Returns:
        True if the header is a recognized standard header, False otherwise.
    """
    return header_name.lower() in HEADER_DESCRIPTIONS
