import webbrowser

from rich.style import Style
from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.content import Content
from textual.widgets.data_table import CellDoesNotExist
from textual_autocomplete import DropdownItem, AutoComplete, TargetState
from posting.collection import Header
from posting.help_data import HelpData
from posting.mdn_headers import get_mdn_url, has_mdn_docs

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


class HeadersTable(PostingDataTable):
    """
    The headers table.
    """

    help = HelpData(
        title="Headers Table",
        description="""\
A table of HTTP headers that will be sent with the request.
Press `backspace` to delete a header.
Press `space` to toggle a header on and off.
Press `enter` to open the MDN documentation page for the selected header in your browser.
Headers with MDN documentation are shown with an underline.
Posting will automatically attach a `User-Agent` header to outgoing requests in order to identify itself, and set the `Content-Type` depending on the content
in the body tab. Setting a header in this table will override the default value in these cases.
""",
    )

    BINDING_GROUP_TITLE = "Headers Table"

    BINDINGS = [
        Binding("backspace", action="remove_row", description="Remove header"),
        Binding("space", action="toggle_row", description="Toggle header"),
        Binding("enter", action="open_mdn_docs", description="Open MDN docs"),
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
        sender=None,
    ):
        """Add a row, styling header names that have MDN documentation."""
        styled_cells = list(cells)

        # Style the header name (first cell) if it has MDN docs
        if styled_cells:
            header_name = styled_cells[0]
            if isinstance(header_name, str):
                header_text = Text(header_name)
            else:
                header_text = header_name

            # Add underline style if MDN docs exist for this header
            if has_mdn_docs(header_text.plain):
                header_text.stylize(Style(underline=True))

            styled_cells[0] = header_text

        return super().add_row(
            *styled_cells,
            height=height,
            key=key,
            label=label,
            explicit_by_user=explicit_by_user,
            sender=sender,
        )

    def action_open_mdn_docs(self) -> None:
        """Open the MDN documentation for the currently selected header."""
        try:
            cursor_cell_key = self.coordinate_to_cell_key(self.cursor_coordinate)
            cursor_row_key, _ = cursor_cell_key
            row = self.get_row(cursor_row_key)
        except CellDoesNotExist:
            return

        if not row:
            return

        header_name = row[0]
        if isinstance(header_name, Text):
            header_name = header_name.plain

        url = get_mdn_url(header_name)
        if url:
            webbrowser.open(url)
            self.notify(
                f"Opening MDN docs for '{header_name}'",
                title="Opening browser",
                timeout=2,
            )
        else:
            self.notify(
                f"No MDN documentation available for '{header_name}'",
                title="No docs available",
                severity="warning",
                timeout=2,
            )

    def watch_has_focus(self, value: bool) -> None:
        self._scroll_cursor_into_view()
        return super().watch_has_focus(value)

    def as_dict(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        for row_index in range(self.row_count):
            row = self.get_row_at(row_index)
            if self.is_row_enabled_at(row_index):
                headers[row[0]] = row[1]
        return headers

    def to_model(self) -> list[Header]:
        headers: list[Header] = []
        for row_index in range(self.row_count):
            row = self.get_row_at(row_index)
            plain_row0 = row[0].plain if isinstance(row[0], Text) else row[0]
            plain_row1 = row[1].plain if isinstance(row[1], Text) else row[1]
            is_row_enabled = self.is_row_enabled_at(row_index)
            headers.append(
                Header(name=plain_row0, value=plain_row1, enabled=is_row_enabled)
            )
        return headers
