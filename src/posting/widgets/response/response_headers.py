import webbrowser

from rich.style import Style
from rich.text import Text
from textual.binding import Binding
from textual.widgets.data_table import CellDoesNotExist

from posting.help_data import HelpData
from posting.mdn_headers import get_mdn_url, has_mdn_docs
from posting.widgets.datatable import PostingDataTable


class ResponseHeadersTable(PostingDataTable):
    """Table displaying response headers with MDN documentation links."""

    help = HelpData(
        title="Response Headers Table",
        description="""\
A table displaying HTTP headers received in the response.
Headers with MDN documentation are shown with an underline.
Press `enter` to open the MDN documentation page for the selected header in your browser.
""",
    )

    BINDING_GROUP_TITLE = "Response Headers Table"

    BINDINGS = [
        Binding(
            "enter",
            action="open_mdn_docs",
            description="Open MDN docs",
        ),
    ]

    def on_mount(self) -> None:
        self.show_header = False
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.fixed_columns = 1
        self.add_columns(*["Header", "Value"])
        self.cursor_vertical_escape = False

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
