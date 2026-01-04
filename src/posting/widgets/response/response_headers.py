from typing import Iterable

from rich.text import Text
from textual.widgets.data_table import RowKey

from posting.mdn_header_links import MDNLinkMixin
from posting.help_data import HelpData
from posting.widgets.datatable import PostingDataTable


class ResponseHeadersTable(MDNLinkMixin, PostingDataTable):
    """
    The response headers table.
    Inherits MDN link functionality from MDNLinkMixin.
    """

    help = HelpData(
        title="Response Headers Table",
        description="""\
A table of HTTP headers received in the response.
Press `enter` to open MDN documentation for standard headers.
""",
    )

    BINDING_GROUP_TITLE = "Response Headers Table"

    BINDINGS = [
        *MDNLinkMixin.MDN_BINDINGS,
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
    ) -> RowKey:
        """Add a row with MDN link indicator for standard headers."""
        return self._add_row_with_mdn_indicator(
            *cells,
            height=height,
            key=key,
            label=label,
            explicit_by_user=explicit_by_user,
        )

    def add_rows(
        self, rows: Iterable[Iterable[str | Text]], *, explicit_by_user: bool = True
    ) -> list[RowKey]:
        """Add multiple rows with MDN link indicators for standard headers."""
        row_keys = []
        for row in rows:
            row_list = list(row)
            row_keys.append(self.add_row(*row_list, explicit_by_user=explicit_by_user))
        return row_keys
