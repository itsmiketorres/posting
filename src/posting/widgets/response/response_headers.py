from rich.text import Text

from posting.auto_headers import is_auto_response_header
from posting.widgets.datatable import PostingDataTable


class ResponseHeadersTable(PostingDataTable):
    def on_mount(self) -> None:
        self.show_header = False
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.fixed_columns = 1
        self.add_columns(*["Header", "Value"])
        self.cursor_vertical_escape = False

    def add_header_row(self, name: str, value: str) -> None:
        """Add a header row, styling it as dim if it's an auto-set header."""
        if is_auto_response_header(name):
            name_text = Text(name, style="dim")
            value_text = Text(value, style="dim")
            self.add_row(name_text, value_text, explicit_by_user=False)
        else:
            self.add_row(name, value, explicit_by_user=False)
