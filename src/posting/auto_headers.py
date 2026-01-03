"""
Detect headers that are automatically set by HTTP clients and servers.

This module uses the `requests` library to determine which headers are
automatically added to requests and which headers are typically added
by servers in responses.
"""

import requests


def _get_auto_request_headers() -> dict[str, str]:
    """
    Make a prepared request to example.com using the requests library
    and return a mapping of all headers that are automatically set.

    Returns:
        A dictionary mapping header names (lowercase) to their auto-set values.
    """
    session = requests.Session()
    req = requests.Request("GET", "https://example.com")
    prepared = session.prepare_request(req)

    # Return headers as lowercase keys for case-insensitive matching
    return {name.lower(): value for name, value in prepared.headers.items()}


def _get_auto_response_headers() -> dict[str, str]:
    """
    Make a request to example.com and return a mapping of all headers
    in the response, representing typical server-set headers.

    Returns:
        A dictionary mapping header names (lowercase) to their values.
    """
    try:
        response = requests.get("https://example.com", timeout=5)
        return {name.lower(): value for name, value in response.headers.items()}
    except requests.RequestException:
        # Fallback to common response headers if request fails
        return {
            "content-type": "",
            "content-length": "",
            "date": "",
            "server": "",
            "cache-control": "",
            "expires": "",
            "last-modified": "",
            "etag": "",
            "vary": "",
            "connection": "",
            "keep-alive": "",
            "transfer-encoding": "",
            "content-encoding": "",
            "x-cache": "",
            "age": "",
        }


# Headers automatically set by request libraries (from requests PreparedRequest)
AUTO_REQUEST_HEADERS: dict[str, str] = _get_auto_request_headers()

# Headers typically set by servers in responses (from example.com response)
AUTO_RESPONSE_HEADERS: dict[str, str] = _get_auto_response_headers()


def is_auto_request_header(header_name: str) -> bool:
    """
    Check if a header name is one that is automatically set by request libraries.

    Args:
        header_name: The name of the header to check.

    Returns:
        True if the header is typically auto-set by HTTP clients.
    """
    return header_name.lower() in AUTO_REQUEST_HEADERS


def is_auto_response_header(header_name: str) -> bool:
    """
    Check if a header name is one that is typically set by servers.

    Args:
        header_name: The name of the header to check.

    Returns:
        True if the header is typically auto-set by HTTP servers.
    """
    return header_name.lower() in AUTO_RESPONSE_HEADERS
