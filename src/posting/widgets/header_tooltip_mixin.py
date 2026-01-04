"""
Mixin class to provide header tooltip functionality for DataTable widgets.

This mixin adds tooltip display for HTTP headers, showing descriptions
for standard headers and indicating when headers are custom/non-standard.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.text import Text
from textual.coordinate import Coordinate
from textual.css.query import NoMatches
from textual.widgets import Label

from posting.header_info import get_header_description, is_standard_header

if TYPE_CHECKING:
    from textual.widgets import DataTable

# CSS for the tooltip label
TOOLTIP_LABEL_CSS = """
HeaderTooltipLabel {
    height: 1;
    width: 100%;
    background: $surface;
    color: $text-muted;
    padding: 0 1;
    text-style: italic;
    &.hidden {
        display: none;
    }
}
"""


class HeaderTooltipLabel(Label):
    """A label widget for displaying header tooltips."""

    DEFAULT_CSS = TOOLTIP_LABEL_CSS


class HeaderTooltipMixin:
    """
    Mixin class that provides header tooltip functionality.

    This mixin should be added to DataTable-based widgets that display
    HTTP headers. It watches cursor changes and displays a tooltip label
    showing the header description.

    The tooltip shows:
    - A description for standard HTTP headers
    - "Custom header (non-standard)." for unrecognized headers
    """

    _tooltip_label: HeaderTooltipLabel | None = None

    def watch_cursor_coordinate(
        self: "DataTable",
        old_coordinate: Coordinate,
        new_coordinate: Coordinate,
    ) -> None:
        """Watch for cursor coordinate changes and update the header tooltip."""
        # Call parent implementation if it exists
        super().watch_cursor_coordinate(old_coordinate, new_coordinate)  # type: ignore[misc]

        # Only update tooltip if we have focus
        if self.has_focus:
            self._update_header_tooltip()

    def watch_has_focus(self: "DataTable", value: bool) -> None:
        """Watch for focus changes and update/clear the tooltip accordingly."""
        # Call parent implementation first
        super().watch_has_focus(value)  # type: ignore[misc]

        if value:
            # Widget gained focus - show tooltip
            self._update_header_tooltip()
        else:
            # Widget lost focus - clear tooltip
            self._clear_header_tooltip()

    def _get_or_create_tooltip_label(self: "DataTable") -> HeaderTooltipLabel | None:
        """Get the tooltip label, creating it if necessary."""
        if self._tooltip_label is not None:
            return self._tooltip_label

        # Try to find an existing tooltip label in our parent
        try:
            parent = self.parent
            if parent is not None:
                self._tooltip_label = parent.query_one(
                    f"HeaderTooltipLabel.{self._tooltip_label_class}",
                    HeaderTooltipLabel,
                )
                return self._tooltip_label
        except NoMatches:
            pass

        # Create a new tooltip label and mount it after the table
        if self.parent is not None:
            label = HeaderTooltipLabel("", classes=f"hidden {self._tooltip_label_class}")
            self.parent.mount(label, after=self)
            self._tooltip_label = label
            return label

        return None

    @property
    def _tooltip_label_class(self: "DataTable") -> str:
        """Return a unique class name for this table's tooltip label."""
        return f"tooltip-for-{self.id or id(self)}"

    def _update_header_tooltip(self: "DataTable") -> None:
        """Update the tooltip based on the currently selected header."""
        if self.row_count == 0:
            self._clear_header_tooltip()
            return

        try:
            row_index = self.cursor_coordinate.row
            if row_index < 0 or row_index >= self.row_count:
                self._clear_header_tooltip()
                return

            row = self.get_row_at(row_index)
            if not row:
                self._clear_header_tooltip()
                return

            # Get the header name from the first column
            header_name = row[0]
            if isinstance(header_name, Text):
                header_name = header_name.plain

            if not header_name:
                self._clear_header_tooltip()
                return

            description = get_header_description(header_name)
            is_standard = is_standard_header(header_name)

            # Format the tooltip with header type indication
            if is_standard:
                tooltip_text = f"[b]{header_name}[/]: {description}"
            else:
                tooltip_text = f"[b]{header_name}[/]: [dim italic]{description}[/]"

            self._set_header_tooltip(tooltip_text)

        except Exception:
            # If anything goes wrong, just clear the tooltip
            self._clear_header_tooltip()

    def _set_header_tooltip(self: "DataTable", text: str) -> None:
        """Set the tooltip text in the tooltip label."""
        label = self._get_or_create_tooltip_label()
        if label is not None:
            label.update(text)
            label.remove_class("hidden")

    def _clear_header_tooltip(self: "DataTable") -> None:
        """Clear and hide the tooltip label."""
        if self._tooltip_label is not None:
            self._tooltip_label.update("")
            self._tooltip_label.add_class("hidden")

    def on_mount(self: "DataTable") -> None:
        """Initialize the tooltip on mount."""
        super().on_mount()  # type: ignore[misc]
        # Set initial tooltip if there are rows and we have focus
        if self.row_count > 0 and self.has_focus:
            self._update_header_tooltip()
