"""
MDN documentation links for standard HTTP headers.
Maps header names (case-insensitive) to their MDN documentation URLs.
"""

import webbrowser
from typing import TYPE_CHECKING

from rich.text import Text
from textual.binding import Binding
from textual.widgets.data_table import CellDoesNotExist

if TYPE_CHECKING:
    from textual.widgets.data_table import RowKey

MDN_BASE_URL = "https://developer.mozilla.org"

# HashMap of standard HTTP header names to their MDN documentation paths
# Keys are lowercase for case-insensitive lookup
MDN_HEADER_LINKS: dict[str, str] = {
    # Authentication
    "authorization": "/en-US/docs/Web/HTTP/Headers/Authorization",
    "proxy-authorization": "/en-US/docs/Web/HTTP/Headers/Proxy-Authorization",
    "proxy-authenticate": "/en-US/docs/Web/HTTP/Headers/Proxy-Authenticate",
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
    # Message body information
    "content-disposition": "/en-US/docs/Web/HTTP/Headers/Content-Disposition",
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
    "accept-ranges": "/en-US/docs/Web/HTTP/Headers/Accept-Ranges",
    "if-range": "/en-US/docs/Web/HTTP/Headers/If-Range",
    "range": "/en-US/docs/Web/HTTP/Headers/Range",
    # Security
    "content-security-policy": "/en-US/docs/Web/HTTP/Headers/Content-Security-Policy",
    "content-security-policy-report-only": "/en-US/docs/Web/HTTP/Headers/Content-Security-Policy-Report-Only",
    "cross-origin-embedder-policy": "/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy",
    "cross-origin-opener-policy": "/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy",
    "cross-origin-resource-policy": "/en-US/docs/Web/HTTP/Headers/Cross-Origin-Resource-Policy",
    "permissions-policy": "/en-US/docs/Web/HTTP/Headers/Permissions-Policy",
    "strict-transport-security": "/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security",
    "upgrade-insecure-requests": "/en-US/docs/Web/HTTP/Headers/Upgrade-Insecure-Requests",
    "x-content-type-options": "/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options",
    "x-frame-options": "/en-US/docs/Web/HTTP/Headers/X-Frame-Options",
    "x-xss-protection": "/en-US/docs/Web/HTTP/Headers/X-XSS-Protection",
    # Fetch metadata request headers
    "sec-fetch-dest": "/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Dest",
    "sec-fetch-mode": "/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Mode",
    "sec-fetch-site": "/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Site",
    "sec-fetch-user": "/en-US/docs/Web/HTTP/Headers/Sec-Fetch-User",
    # Transfer coding
    "te": "/en-US/docs/Web/HTTP/Headers/TE",
    "trailer": "/en-US/docs/Web/HTTP/Headers/Trailer",
    "transfer-encoding": "/en-US/docs/Web/HTTP/Headers/Transfer-Encoding",
    # Other
    "alt-svc": "/en-US/docs/Web/HTTP/Headers/Alt-Svc",
    "alt-used": "/en-US/docs/Web/HTTP/Headers/Alt-Used",
    "date": "/en-US/docs/Web/HTTP/Headers/Date",
    "link": "/en-US/docs/Web/HTTP/Headers/Link",
    "retry-after": "/en-US/docs/Web/HTTP/Headers/Retry-After",
    "server-timing": "/en-US/docs/Web/HTTP/Headers/Server-Timing",
    "sourcemap": "/en-US/docs/Web/HTTP/Headers/SourceMap",
    "upgrade": "/en-US/docs/Web/HTTP/Headers/Upgrade",
    # Non-standard but documented headers
    "x-forwarded-for": "/en-US/docs/Web/HTTP/Headers/X-Forwarded-For",
    "x-forwarded-host": "/en-US/docs/Web/HTTP/Headers/X-Forwarded-Host",
    "x-forwarded-proto": "/en-US/docs/Web/HTTP/Headers/X-Forwarded-Proto",
    # Deprecated headers
    "pragma": "/en-US/docs/Web/HTTP/Headers/Pragma",
    "warning": "/en-US/docs/Web/HTTP/Headers/Warning",
    # Privacy
    "dnt": "/en-US/docs/Web/HTTP/Headers/DNT",
    "tk": "/en-US/docs/Web/HTTP/Headers/Tk",
    "sec-gpc": "/en-US/docs/Web/HTTP/Headers/Sec-GPC",
    # Client hints
    "accept-ch": "/en-US/docs/Web/HTTP/Headers/Accept-CH",
    "critical-ch": "/en-US/docs/Web/HTTP/Headers/Critical-CH",
    # Service Workers
    "service-worker-navigation-preload": "/en-US/docs/Web/HTTP/Headers/Service-Worker-Navigation-Preload",
    # Experimental
    "early-data": "/en-US/docs/Web/HTTP/Headers/Early-Data",
    "nel": "/en-US/docs/Web/HTTP/Headers/NEL",
    "report-to": "/en-US/docs/Web/HTTP/Headers/Report-To",
}


def get_mdn_link(header_name: str) -> str | None:
    """
    Get the full MDN documentation URL for a header name.
    Returns None if the header is not a standard header with documentation.

    Args:
        header_name: The HTTP header name (case-insensitive)

    Returns:
        The full MDN URL or None if not found
    """
    path = MDN_HEADER_LINKS.get(header_name.lower())
    if path:
        return f"{MDN_BASE_URL}{path}"
    return None


class MDNLinkMixin:
    """
    Mixin class providing MDN documentation link functionality for header tables.

    This mixin adds:
    - A cyan arrow indicator (➚) next to standard HTTP headers that have MDN documentation
    - An action to open MDN docs in the browser when Enter is pressed
    - Helper methods for managing the indicator in header names

    Classes using this mixin should:
    - Inherit from both this mixin and PostingDataTable (mixin first)
    - Call super() appropriately in overridden methods
    """

    # Arrow indicator suffix for linkable headers (cyan north-east arrow)
    # Using ➚ which is more vertically centered than ↗
    LINK_INDICATOR = " ➚"
    LINK_INDICATOR_STYLE = "cyan"

    # Bindings for MDN docs action - subclasses should include this in their BINDINGS
    MDN_BINDINGS = [
        Binding("enter", action="open_mdn_docs", description="Open MDN docs"),
    ]

    def _strip_link_indicator(self, text: str | Text) -> str:
        """Strip the MDN link indicator from a header name."""
        if isinstance(text, Text):
            plain = text.plain
        else:
            plain = str(text)
        if plain.endswith(self.LINK_INDICATOR):
            return plain[: -len(self.LINK_INDICATOR)]
        return plain

    def _make_header_with_indicator(self, header_name: str) -> Text:
        """Create a Text header name with MDN link indicator if the header is standard."""
        if get_mdn_link(header_name):
            result = Text(header_name)
            result.append(self.LINK_INDICATOR, style=self.LINK_INDICATOR_STYLE)
            return result
        return Text(header_name)

    def _get_current_header_name(self) -> str | None:
        """Get the header name at the current cursor position (without indicator)."""
        try:
            cursor_cell_key = self.coordinate_to_cell_key(self.cursor_coordinate)
            cursor_row_key, _ = cursor_cell_key
            row = self.get_row(cursor_row_key)
            header_name = row[0]
            return self._strip_link_indicator(header_name)
        except CellDoesNotExist:
            return None

    def action_open_mdn_docs(self) -> None:
        """Open MDN documentation for the current header."""
        header_name = self._get_current_header_name()
        if header_name:
            mdn_url = get_mdn_link(header_name)
            if mdn_url:
                webbrowser.open(mdn_url)

    def _add_row_with_mdn_indicator(
        self,
        *cells: str | Text,
        height: int | None = 1,
        key: str | None = None,
        label: str | Text | None = None,
        explicit_by_user: bool = True,
    ) -> "RowKey":
        """
        Add a row with MDN link indicator for standard headers.
        This should be called from the subclass's add_row method.
        """
        if len(cells) >= 1:
            header_name = cells[0]
            if isinstance(header_name, Text):
                header_name_str = header_name.plain
            else:
                header_name_str = str(header_name)

            modified_header = self._make_header_with_indicator(header_name_str)
            cells = (modified_header,) + cells[1:]

        # Call the parent class's add_row (PostingDataTable)
        return super().add_row(
            *cells,
            height=height,
            key=key,
            label=label,
            explicit_by_user=explicit_by_user,
        )
