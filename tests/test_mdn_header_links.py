"""
Tests for MDN header links functionality.

Tests that:
- Standard headers get the MDN link indicator
- Custom headers do NOT get the MDN link indicator
- The enter key opens MDN docs for standard headers
- The enter key does NOT attempt to open MDN for custom headers
- Header data is correctly extracted without the indicator
"""

import pytest
from unittest.mock import patch, MagicMock
from rich.text import Text

from posting.mdn_header_links import (
    get_mdn_link,
    MDN_HEADER_LINKS,
    MDN_BASE_URL,
    MDNLinkMixin,
)


class TestGetMdnLink:
    """Tests for the get_mdn_link function."""

    def test_returns_url_for_standard_header(self):
        """Standard headers should return their MDN URL."""
        url = get_mdn_link("Content-Type")
        assert url is not None
        assert url == f"{MDN_BASE_URL}/en-US/docs/Web/HTTP/Headers/Content-Type"

    def test_returns_url_case_insensitive(self):
        """Header lookup should be case-insensitive."""
        url1 = get_mdn_link("content-type")
        url2 = get_mdn_link("CONTENT-TYPE")
        url3 = get_mdn_link("Content-Type")
        assert url1 == url2 == url3
        assert url1 is not None

    def test_returns_none_for_custom_header(self):
        """Custom headers should return None."""
        assert get_mdn_link("foo") is None
        assert get_mdn_link("bar") is None
        assert get_mdn_link("baz") is None
        assert get_mdn_link("X-Custom-Header") is None
        assert get_mdn_link("My-Custom-Header") is None

    def test_returns_none_for_empty_string(self):
        """Empty string should return None."""
        assert get_mdn_link("") is None

    @pytest.mark.parametrize(
        "header_name",
        [
            "Content-Type",
            "Accept",
            "Authorization",
            "Cache-Control",
            "User-Agent",
            "Host",
            "Cookie",
            "Set-Cookie",
            "Content-Length",
            "Accept-Encoding",
        ],
    )
    def test_common_headers_have_links(self, header_name):
        """Common standard headers should have MDN links."""
        url = get_mdn_link(header_name)
        assert url is not None
        assert url.startswith(MDN_BASE_URL)

    @pytest.mark.parametrize(
        "header_name",
        [
            "foo",
            "bar",
            "baz",
            "X-Custom",
            "X-My-Header",
            "Custom-Header",
            "Not-A-Real-Header",
        ],
    )
    def test_custom_headers_have_no_links(self, header_name):
        """Custom/non-standard headers should not have MDN links."""
        assert get_mdn_link(header_name) is None


class TestMDNHeaderLinksMap:
    """Tests for the MDN_HEADER_LINKS dictionary."""

    def test_all_keys_are_lowercase(self):
        """All keys in the map should be lowercase for consistent lookup."""
        for key in MDN_HEADER_LINKS.keys():
            assert key == key.lower(), f"Key '{key}' is not lowercase"

    def test_all_values_are_valid_paths(self):
        """All values should be valid MDN path strings."""
        for key, path in MDN_HEADER_LINKS.items():
            assert path.startswith("/en-US/docs/Web/HTTP/Headers/"), (
                f"Path for '{key}' doesn't start with expected prefix: {path}"
            )

    def test_map_has_reasonable_size(self):
        """The map should contain a reasonable number of headers."""
        # Should have at least 50 standard headers
        assert len(MDN_HEADER_LINKS) >= 50


class TestMDNLinkMixin:
    """Tests for the MDNLinkMixin class."""

    def test_link_indicator_constant(self):
        """Link indicator should be defined."""
        assert hasattr(MDNLinkMixin, "LINK_INDICATOR")
        assert MDNLinkMixin.LINK_INDICATOR == " ➚"

    def test_link_indicator_style(self):
        """Link indicator style should be cyan."""
        assert hasattr(MDNLinkMixin, "LINK_INDICATOR_STYLE")
        assert MDNLinkMixin.LINK_INDICATOR_STYLE == "cyan"

    def test_mdn_bindings_defined(self):
        """MDN bindings should be defined for enter key."""
        assert hasattr(MDNLinkMixin, "MDN_BINDINGS")
        bindings = MDNLinkMixin.MDN_BINDINGS
        assert len(bindings) == 1
        assert bindings[0].key == "enter"
        assert bindings[0].action == "open_mdn_docs"


class TestMDNLinkMixinMethods:
    """Tests for MDNLinkMixin methods using a mock table."""

    @pytest.fixture
    def mixin_instance(self):
        """Create a mock instance with MDNLinkMixin methods."""
        # Create a simple class that has the mixin methods
        instance = MagicMock()
        instance.LINK_INDICATOR = MDNLinkMixin.LINK_INDICATOR
        instance.LINK_INDICATOR_STYLE = MDNLinkMixin.LINK_INDICATOR_STYLE
        instance._strip_link_indicator = lambda text: MDNLinkMixin._strip_link_indicator(
            instance, text
        )
        instance._make_header_with_indicator = (
            lambda header_name: MDNLinkMixin._make_header_with_indicator(
                instance, header_name
            )
        )
        return instance

    def test_strip_link_indicator_with_indicator(self, mixin_instance):
        """Should strip the indicator from header names that have it."""
        header_with_indicator = f"Content-Type{MDNLinkMixin.LINK_INDICATOR}"
        result = mixin_instance._strip_link_indicator(header_with_indicator)
        assert result == "Content-Type"

    def test_strip_link_indicator_without_indicator(self, mixin_instance):
        """Should return unchanged header names that don't have indicator."""
        result = mixin_instance._strip_link_indicator("Content-Type")
        assert result == "Content-Type"

    def test_strip_link_indicator_with_text_object(self, mixin_instance):
        """Should handle Text objects correctly."""
        text = Text(f"Content-Type{MDNLinkMixin.LINK_INDICATOR}")
        result = mixin_instance._strip_link_indicator(text)
        assert result == "Content-Type"

    def test_strip_link_indicator_custom_header(self, mixin_instance):
        """Custom headers without indicator should be unchanged."""
        result = mixin_instance._strip_link_indicator("foo")
        assert result == "foo"

    def test_make_header_with_indicator_standard(self, mixin_instance):
        """Standard headers should get the indicator."""
        result = mixin_instance._make_header_with_indicator("Content-Type")
        assert isinstance(result, Text)
        assert result.plain == f"Content-Type{MDNLinkMixin.LINK_INDICATOR}"

    def test_make_header_with_indicator_custom(self, mixin_instance):
        """Custom headers should NOT get the indicator."""
        result = mixin_instance._make_header_with_indicator("foo")
        assert isinstance(result, Text)
        assert result.plain == "foo"
        assert MDNLinkMixin.LINK_INDICATOR not in result.plain

    @pytest.mark.parametrize("custom_header", ["foo", "bar", "baz", "X-Custom"])
    def test_custom_headers_no_indicator(self, mixin_instance, custom_header):
        """Various custom headers should not get indicators."""
        result = mixin_instance._make_header_with_indicator(custom_header)
        assert result.plain == custom_header
        assert MDNLinkMixin.LINK_INDICATOR not in result.plain


class TestActionOpenMdnDocs:
    """Tests for the action_open_mdn_docs action."""

    def test_opens_browser_for_standard_header(self):
        """Should open browser with MDN URL for standard headers."""
        # Create a mock instance
        instance = MagicMock()
        instance.LINK_INDICATOR = MDNLinkMixin.LINK_INDICATOR
        instance._strip_link_indicator = lambda text: MDNLinkMixin._strip_link_indicator(
            instance, text
        )
        instance._get_current_header_name = MagicMock(return_value="Content-Type")

        with patch("posting.mdn_header_links.webbrowser.open") as mock_open:
            MDNLinkMixin.action_open_mdn_docs(instance)
            mock_open.assert_called_once()
            call_url = mock_open.call_args[0][0]
            assert "Content-Type" in call_url
            assert MDN_BASE_URL in call_url

    def test_does_not_open_browser_for_custom_header(self):
        """Should NOT open browser for custom headers."""
        instance = MagicMock()
        instance.LINK_INDICATOR = MDNLinkMixin.LINK_INDICATOR
        instance._strip_link_indicator = lambda text: MDNLinkMixin._strip_link_indicator(
            instance, text
        )
        instance._get_current_header_name = MagicMock(return_value="foo")

        with patch("posting.mdn_header_links.webbrowser.open") as mock_open:
            MDNLinkMixin.action_open_mdn_docs(instance)
            mock_open.assert_not_called()

    def test_does_not_open_browser_when_no_header_selected(self):
        """Should NOT open browser when no header is selected."""
        instance = MagicMock()
        instance._get_current_header_name = MagicMock(return_value=None)

        with patch("posting.mdn_header_links.webbrowser.open") as mock_open:
            MDNLinkMixin.action_open_mdn_docs(instance)
            mock_open.assert_not_called()

    @pytest.mark.parametrize("custom_header", ["foo", "bar", "baz", "X-Custom", "My-Header"])
    def test_custom_headers_do_not_trigger_browser(self, custom_header):
        """Various custom headers should not trigger browser open."""
        instance = MagicMock()
        instance.LINK_INDICATOR = MDNLinkMixin.LINK_INDICATOR
        instance._strip_link_indicator = lambda text: MDNLinkMixin._strip_link_indicator(
            instance, text
        )
        instance._get_current_header_name = MagicMock(return_value=custom_header)

        with patch("posting.mdn_header_links.webbrowser.open") as mock_open:
            MDNLinkMixin.action_open_mdn_docs(instance)
            mock_open.assert_not_called()

    @pytest.mark.parametrize(
        "standard_header",
        ["Content-Type", "Accept", "Authorization", "Cache-Control", "User-Agent"],
    )
    def test_standard_headers_trigger_browser(self, standard_header):
        """Standard headers should trigger browser open with correct URL."""
        instance = MagicMock()
        instance.LINK_INDICATOR = MDNLinkMixin.LINK_INDICATOR
        instance._strip_link_indicator = lambda text: MDNLinkMixin._strip_link_indicator(
            instance, text
        )
        instance._get_current_header_name = MagicMock(return_value=standard_header)

        with patch("posting.mdn_header_links.webbrowser.open") as mock_open:
            MDNLinkMixin.action_open_mdn_docs(instance)
            mock_open.assert_called_once()
            call_url = mock_open.call_args[0][0]
            assert MDN_BASE_URL in call_url


class TestIndicatorInHeaderDisplay:
    """Tests to verify indicator appears correctly in displayed headers."""

    def test_standard_header_has_indicator_in_plain_text(self):
        """Standard headers should show indicator in plain text."""
        mixin = MagicMock()
        mixin.LINK_INDICATOR = MDNLinkMixin.LINK_INDICATOR
        mixin.LINK_INDICATOR_STYLE = MDNLinkMixin.LINK_INDICATOR_STYLE

        result = MDNLinkMixin._make_header_with_indicator(mixin, "Content-Type")
        assert MDNLinkMixin.LINK_INDICATOR in result.plain

    def test_custom_header_has_no_indicator(self):
        """Custom headers should NOT show indicator."""
        mixin = MagicMock()
        mixin.LINK_INDICATOR = MDNLinkMixin.LINK_INDICATOR
        mixin.LINK_INDICATOR_STYLE = MDNLinkMixin.LINK_INDICATOR_STYLE

        for custom in ["foo", "bar", "baz", "X-Custom"]:
            result = MDNLinkMixin._make_header_with_indicator(mixin, custom)
            assert MDNLinkMixin.LINK_INDICATOR not in result.plain
            assert result.plain == custom


class TestDataIntegrity:
    """Tests to ensure header data is not corrupted by indicators."""

    def test_stripped_header_matches_original(self):
        """After stripping indicator, header name should match original."""
        mixin = MagicMock()
        mixin.LINK_INDICATOR = MDNLinkMixin.LINK_INDICATOR
        mixin.LINK_INDICATOR_STYLE = MDNLinkMixin.LINK_INDICATOR_STYLE

        original = "Content-Type"
        with_indicator = MDNLinkMixin._make_header_with_indicator(mixin, original)
        stripped = MDNLinkMixin._strip_link_indicator(mixin, with_indicator)

        assert stripped == original

    def test_custom_header_unchanged_after_roundtrip(self):
        """Custom headers should be unchanged after make/strip roundtrip."""
        mixin = MagicMock()
        mixin.LINK_INDICATOR = MDNLinkMixin.LINK_INDICATOR
        mixin.LINK_INDICATOR_STYLE = MDNLinkMixin.LINK_INDICATOR_STYLE

        for custom in ["foo", "bar", "baz"]:
            with_indicator = MDNLinkMixin._make_header_with_indicator(mixin, custom)
            stripped = MDNLinkMixin._strip_link_indicator(mixin, with_indicator)
            assert stripped == custom
