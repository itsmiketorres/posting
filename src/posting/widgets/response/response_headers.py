from posting.widgets.datatable import PostingDataTable
from posting.widgets.header_tooltip_mixin import HeaderTooltipMixin


class ResponseHeadersTable(HeaderTooltipMixin, PostingDataTable):
    def on_mount(self) -> None:
        self.show_header = False
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.fixed_columns = 1
        self.add_columns(*["Header", "Value"])
        self.cursor_vertical_escape = False
        super().on_mount()
