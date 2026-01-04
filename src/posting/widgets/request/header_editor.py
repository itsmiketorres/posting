from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.content import Content
from textual.coordinate import Coordinate
from textual.widgets.data_table import RowKey
from textual_autocomplete import DropdownItem, AutoComplete, TargetState
from posting.collection import Header
from posting.mdn_header_links import MDNLinkMixin
from posting.help_data import HelpData

from posting.widgets.datatable import PostingDataTable
from posting.request_headers import REQUEST_HEADERS
from posting.widgets.key_value import KeyValueEditor, KeyValueInput
from posting.widgets.input import PostingInput
from posting.widgets.variable_input import VariableInput


HEADER_SUGGESTIONS = {
    "accept": [
        # Common prefixes for autocompletion
        "application/",
        "audio/",
        "font/",
        "image/",
        "text/",
        "video/",
        "multipart/",
        # Common wildcards
        "*",
        "*/*",
        "image/*",
        "audio/*",
        "video/*",
        # Application types
        "application/json",
        "application/xml",
        "application/x-www-form-urlencoded",
        "application/javascript",
        "application/pdf",
        "application/zip",
        "application/octet-stream",
        "application/graphql",
        "application/msgpack",
        # Text types
        "text/plain",
        "text/html",
        "text/css",
        "text/csv",
        "text/markdown",
        "text/yaml",
    ],
    "accept-encoding": [
        # Single encodings
        "gzip",
        "deflate",
        "br",
        "compress",
        "identity",
        "*",
        # Common combinations
        "gzip, deflate",
        "gzip, deflate, br",
    ],
    "accept-language": [
        # Common single languages
        "en",
        "en-US",
        "en-GB",
        "es",
        "es-ES",
        "fr",
        "fr-FR",
        "de",
        "de-DE",
        "it",
        "ja",
        "ko",
        "zh",
        "zh-CN",
        "zh-TW",
        "*",
    ],
    "authorization": [
        # Auth scheme prefixes
        "Bearer ",
        "Basic ",
        "Digest ",
        "OAuth ",
        "JWT ",
        "ApiKey ",
    ],
    "cache-control": [
        # Single directives
        "no-cache",
        "no-store",
        "no-transform",
        "private",
        "public",
        "must-revalidate",
        "proxy-revalidate",
        "max-age=0",
        # Common combinations
        "no-cache, no-store",
        "private, no-cache",
        "no-cache, must-revalidate",
        # Time-based examples
        "max-age=3600",
        "max-age=86400",
        "max-age=604800",
    ],
    "connection": [
        "keep-alive",
        "close",
        "upgrade",
    ],
    "content-type": [
        # Common prefixes for autocompletion
        "application/",
        "audio/",
        "font/",
        "image/",
        "text/",
        "video/",
        "multipart/",
        # Application types
        "application/json",
        "application/xml",
        "application/x-www-form-urlencoded",
        "application/javascript",
        "application/pdf",
        "application/zip",
        "application/octet-stream",
        "application/graphql",
        "application/msgpack",
        # Text types
        "text/plain",
        "text/html",
        "text/css",
        "text/csv",
        "text/markdown",
        "text/yaml",
        # Multipart types
        "multipart/form-data",
        "multipart/mixed",
        "multipart/alternative",
        # Image types
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
        "image/svg+xml",
        "image/avif",
        # Audio types
        "audio/mpeg",
        "audio/ogg",
        "audio/wav",
        # Video types
        "video/mp4",
        "video/webm",
        "video/ogg",
    ],
    "if-match": [
        "*",
        "W/",  # Weak validator prefix
    ],
    "if-none-match": [
        "*",
        "W/",  # Weak validator prefix
    ],
    "pragma": [
        "no-cache",
    ],
    "range": [
        # Common range patterns
        "bytes=",
        "bytes=0-",
        "bytes=0-499",
        "bytes=-500",
        "bytes=500-999",
        "bytes=0-499,500-999",
    ],
}


class HeaderInput(PostingInput):
    help = HelpData(
        title="HTTP Header Input",
        description="""\
An input field for entering HTTP headers.
Press `up` and `down` to navigate the dropdown list when it's visible.
Press `enter` to insert the selected header.
Press `tab` to both insert *and* shift focus.
""",
    )

    BINDING_GROUP_TITLE = "HTTP Header Input"


class HeaderEditor(Vertical):
    BINDING_GROUP_TITLE = "HTTP Header Editor"

    def compose(self) -> ComposeResult:
        header_key_input = HeaderInput(placeholder="Name", id="header-key-input")
        yield KeyValueEditor(
            HeadersTable(),
            KeyValueInput(
                header_key_input,
                VariableInput(
                    placeholder="Value",
                    id="header-value-input",
                    candidates=self.get_header_value_candidates,
                ),
                button_label="Add",
            ),
            empty_message="No headers",
        )

    def on_mount(self):
        header_input = self.header_key_input
        items: list[DropdownItem] = []
        for header in REQUEST_HEADERS:
            style = "$text-warning" if header["experimental"] else ""
            content = Content.styled(header["name"], style=style)
            items.append(DropdownItem(main=content))

        self.screen.mount(
            AutoComplete(
                header_input,
                candidates=items,
                prevent_default_tab=False,
            )
        )

    def get_header_value_candidates(
        self, target_state: TargetState
    ) -> list[DropdownItem]:
        header_key = self.header_key_input.value.strip().lower()
        candidates = [
            DropdownItem(main=suggestion)
            for suggestion in HEADER_SUGGESTIONS.get(header_key, [])
        ]
        return candidates

    @property
    def header_key_input(self) -> HeaderInput:
        return self.query_one("#header-key-input", HeaderInput)


class HeadersTable(MDNLinkMixin, PostingDataTable):
    """
    The headers table for request headers.
    Inherits MDN link functionality from MDNLinkMixin.
    """

    help = HelpData(
        title="Headers Table",
        description="""\
A table of HTTP headers that will be sent with the request.
Press `backspace` to delete a header.
Press `space` to toggle a header on and off.
Press `enter` to open MDN documentation for standard headers.
Posting will automatically attach a `User-Agent` header to outgoing requests in order to identify itself, and set the `Content-Type` depending on the content
in the body tab. Setting a header in this table will override the default value in these cases.
""",
    )

    BINDING_GROUP_TITLE = "Headers Table"

    BINDINGS = [
        Binding("backspace", action="remove_row", description="Remove header"),
        Binding("space", action="toggle_row", description="Toggle header"),
        *MDNLinkMixin.MDN_BINDINGS,
    ]

    def on_mount(self):
        self.show_header = False
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.fixed_columns = 1
        self.row_disable = True
        self.add_columns(*["Header", "Value"])

    def add_row(
        self,
        *cells: str | Text,
        height: int | None = 1,
        key: str | None = None,
        label: str | Text | None = None,
        explicit_by_user: bool = True,
    ) -> RowKey:
        """Add a row with MDN link indicator for standard headers."""
        return self._add_row_with_mdn_indicator(
            *cells,
            height=height,
            key=key,
            label=label,
            explicit_by_user=explicit_by_user,
        )

    def update_cell_at(
        self,
        coordinate: Coordinate,
        value: str | Text,
        *,
        update_width: bool = False,
    ) -> None:
        """Update a cell, adding MDN link indicator for header name column."""
        # If updating the header name column (column 0), add indicator if it has MDN docs
        if coordinate.column == 0:
            if isinstance(value, Text):
                header_name = value.plain
            else:
                header_name = str(value)
            value = self._make_header_with_indicator(header_name)

        super().update_cell_at(coordinate, value, update_width=update_width)

    def watch_has_focus(self, value: bool) -> None:
        self._scroll_cursor_into_view()
        return super().watch_has_focus(value)

    def as_dict(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        for row_index in range(self.row_count):
            row = self.get_row_at(row_index)
            if self.is_row_enabled_at(row_index):
                # Strip indicator from header name
                header_name = self._strip_link_indicator(row[0])
                header_value = row[1].plain if isinstance(row[1], Text) else str(row[1])
                headers[header_name] = header_value
        return headers

    def to_model(self) -> list[Header]:
        headers: list[Header] = []
        for row_index in range(self.row_count):
            row = self.get_row_at(row_index)
            # Strip indicator from header name
            plain_row0 = self._strip_link_indicator(row[0])
            plain_row1 = row[1].plain if isinstance(row[1], Text) else str(row[1])
            is_row_enabled = self.is_row_enabled_at(row_index)
            headers.append(
                Header(name=plain_row0, value=plain_row1, enabled=is_row_enabled)
            )
        return headers
