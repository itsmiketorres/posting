import os
from pathlib import Path
from unittest import mock

import pytest
from textual.pilot import Pilot
from textual.widgets import Checkbox, Input, Label

from posting.__main__ import make_posting
from posting.widgets.request.request_auth import (
    BearerTokenForm,
    UserNamePasswordForm,
)

TEST_DIR = Path(__file__).parent
CONFIG_DIR = TEST_DIR / "sample-configs"
SAMPLE_COLLECTIONS = TEST_DIR / "sample-collections"


def use_config(file_name: str):
    """Specify which config file to use from the `sample-configs` directory."""
    return mock.patch.dict(
        os.environ, {"POSTING_CONFIG_FILE": str(CONFIG_DIR / file_name)}
    )


@use_config("general.yaml")
class TestUserNamePasswordFormHideValue:
    """Tests for the Hide Value checkbox in UserNamePasswordForm (Basic/Digest Auth)."""

    def test_password_hidden_and_checkbox_defaults(self, snap_compare):
        """Password input should be masked by default and checkbox should be checked."""
        results = {}

        async def run_before(pilot: Pilot):
            # Navigate to Auth tab and select Basic auth
            await pilot.press("ctrl+o", "t")  # jump to 'Auth' tab
            await pilot.pause()
            # Select Basic auth from dropdown
            auth_select = pilot.app.query_one("#auth-type-select")
            auth_select.value = "basic"
            await pilot.pause()

            # Verify password is hidden
            password_input = pilot.app.query_one("#password-input", Input)
            results["password_hidden"] = password_input.password

            # Verify checkbox is checked
            checkbox = pilot.app.query_one(
                "#auth-form-basic #hide-value-checkbox", Checkbox
            )
            results["checkbox_checked"] = checkbox.value
            results["checkbox_label"] = checkbox.label.plain

        snap_compare(
            make_posting(collection=SAMPLE_COLLECTIONS),
            run_before=run_before,
            terminal_size=(80, 40),
        )
        assert results["password_hidden"] is True
        assert results["checkbox_checked"] is True
        assert results["checkbox_label"] == "Hide Value"

    def test_unchecking_checkbox_reveals_password(self, snap_compare):
        """Unchecking the Hide Value checkbox should reveal the password."""
        results = {}

        async def run_before(pilot: Pilot):
            await pilot.press("ctrl+o", "t")  # jump to 'Auth' tab
            await pilot.pause()
            auth_select = pilot.app.query_one("#auth-type-select")
            auth_select.value = "basic"
            await pilot.pause()

            # Set a password value
            form = pilot.app.query_one("#auth-form-basic", UserNamePasswordForm)
            form.set_values("testuser", "secretpassword")
            await pilot.pause()

            # Verify initially hidden
            password_input = pilot.app.query_one("#password-input", Input)
            results["initially_hidden"] = password_input.password

            # Click the checkbox to uncheck it
            checkbox = pilot.app.query_one(
                "#auth-form-basic #hide-value-checkbox", Checkbox
            )
            checkbox.toggle()
            await pilot.pause()

            # Verify now visible
            results["checkbox_after_toggle"] = checkbox.value
            results["password_after_toggle"] = password_input.password

        snap_compare(
            make_posting(collection=SAMPLE_COLLECTIONS),
            run_before=run_before,
            terminal_size=(80, 40),
        )
        assert results["initially_hidden"] is True
        assert results["checkbox_after_toggle"] is False
        assert results["password_after_toggle"] is False

    def test_rechecking_checkbox_hides_password(self, snap_compare):
        """Re-checking the Hide Value checkbox should hide the password again."""
        results = {}

        async def run_before(pilot: Pilot):
            await pilot.press("ctrl+o", "t")  # jump to 'Auth' tab
            await pilot.pause()
            auth_select = pilot.app.query_one("#auth-type-select")
            auth_select.value = "basic"
            await pilot.pause()

            checkbox = pilot.app.query_one(
                "#auth-form-basic #hide-value-checkbox", Checkbox
            )
            password_input = pilot.app.query_one("#password-input", Input)

            # Uncheck then recheck
            checkbox.toggle()
            await pilot.pause()
            results["password_after_first_toggle"] = password_input.password

            checkbox.toggle()
            await pilot.pause()

            # Should be hidden again
            results["checkbox_final"] = checkbox.value
            results["password_final"] = password_input.password

        snap_compare(
            make_posting(collection=SAMPLE_COLLECTIONS),
            run_before=run_before,
            terminal_size=(80, 40),
        )
        assert results["password_after_first_toggle"] is False
        assert results["checkbox_final"] is True
        assert results["password_final"] is True

    def test_username_input_never_hidden(self, snap_compare):
        """Username input should never be masked regardless of checkbox state."""
        results = {}

        async def run_before(pilot: Pilot):
            await pilot.press("ctrl+o", "t")  # jump to 'Auth' tab
            await pilot.pause()
            auth_select = pilot.app.query_one("#auth-type-select")
            auth_select.value = "basic"
            await pilot.pause()

            username_input = pilot.app.query_one("#username-input", Input)
            checkbox = pilot.app.query_one(
                "#auth-form-basic #hide-value-checkbox", Checkbox
            )

            # Initially username should be visible
            results["username_initially"] = username_input.password

            # Toggle checkbox
            checkbox.toggle()
            await pilot.pause()

            # Username should still be visible
            results["username_after_toggle"] = username_input.password

        snap_compare(
            make_posting(collection=SAMPLE_COLLECTIONS),
            run_before=run_before,
            terminal_size=(80, 40),
        )
        assert results["username_initially"] is False
        assert results["username_after_toggle"] is False

    def test_get_values_works_regardless_of_visibility(self, snap_compare):
        """get_values should work correctly whether password is hidden or visible."""
        results = {}

        async def run_before(pilot: Pilot):
            await pilot.press("ctrl+o", "t")  # jump to 'Auth' tab
            await pilot.pause()
            auth_select = pilot.app.query_one("#auth-type-select")
            auth_select.value = "basic"
            await pilot.pause()

            form = pilot.app.query_one("#auth-form-basic", UserNamePasswordForm)
            form.set_values("testuser", "testpass")

            # Test with hidden password
            values_hidden = form.get_values()
            results["username_hidden"] = values_hidden["username"]
            results["password_hidden"] = values_hidden["password"]

            # Reveal password
            checkbox = pilot.app.query_one(
                "#auth-form-basic #hide-value-checkbox", Checkbox
            )
            checkbox.toggle()
            await pilot.pause()

            # Test with visible password
            values_visible = form.get_values()
            results["username_visible"] = values_visible["username"]
            results["password_visible"] = values_visible["password"]

        snap_compare(
            make_posting(collection=SAMPLE_COLLECTIONS),
            run_before=run_before,
            terminal_size=(80, 40),
        )
        assert results["username_hidden"] == "testuser"
        assert results["password_hidden"] == "testpass"
        assert results["username_visible"] == "testuser"
        assert results["password_visible"] == "testpass"


@use_config("general.yaml")
class TestBearerTokenFormHideValue:
    """Tests for the Hide Value checkbox in BearerTokenForm."""

    def test_token_hidden_and_checkbox_defaults(self, snap_compare):
        """Token input should be masked by default and checkbox should be checked."""
        results = {}

        async def run_before(pilot: Pilot):
            await pilot.press("ctrl+o", "t")  # jump to 'Auth' tab
            await pilot.pause()
            auth_select = pilot.app.query_one("#auth-type-select")
            auth_select.value = "bearer-token"
            await pilot.pause()

            token_input = pilot.app.query_one("#token-input", Input)
            results["token_hidden"] = token_input.password

            checkbox = pilot.app.query_one(
                "#auth-form-bearer-token #hide-value-checkbox", Checkbox
            )
            results["checkbox_checked"] = checkbox.value
            results["checkbox_label"] = checkbox.label.plain

        snap_compare(
            make_posting(collection=SAMPLE_COLLECTIONS),
            run_before=run_before,
            terminal_size=(80, 40),
        )
        assert results["token_hidden"] is True
        assert results["checkbox_checked"] is True
        assert results["checkbox_label"] == "Hide Value"

    def test_unchecking_checkbox_reveals_token(self, snap_compare):
        """Unchecking the Hide Value checkbox should reveal the token."""
        results = {}

        async def run_before(pilot: Pilot):
            await pilot.press("ctrl+o", "t")  # jump to 'Auth' tab
            await pilot.pause()
            auth_select = pilot.app.query_one("#auth-type-select")
            auth_select.value = "bearer-token"
            await pilot.pause()

            # Set a token value
            form = pilot.app.query_one("#auth-form-bearer-token", BearerTokenForm)
            form.set_values("my-secret-token")
            await pilot.pause()

            token_input = pilot.app.query_one("#token-input", Input)
            checkbox = pilot.app.query_one(
                "#auth-form-bearer-token #hide-value-checkbox", Checkbox
            )

            # Initially hidden
            results["initially_hidden"] = token_input.password

            # Click to reveal
            checkbox.toggle()
            await pilot.pause()

            # Now visible
            results["checkbox_after_toggle"] = checkbox.value
            results["token_after_toggle"] = token_input.password

        snap_compare(
            make_posting(collection=SAMPLE_COLLECTIONS),
            run_before=run_before,
            terminal_size=(80, 40),
        )
        assert results["initially_hidden"] is True
        assert results["checkbox_after_toggle"] is False
        assert results["token_after_toggle"] is False

    def test_rechecking_checkbox_hides_token(self, snap_compare):
        """Re-checking the Hide Value checkbox should hide the token again."""
        results = {}

        async def run_before(pilot: Pilot):
            await pilot.press("ctrl+o", "t")  # jump to 'Auth' tab
            await pilot.pause()
            auth_select = pilot.app.query_one("#auth-type-select")
            auth_select.value = "bearer-token"
            await pilot.pause()

            token_input = pilot.app.query_one("#token-input", Input)
            checkbox = pilot.app.query_one(
                "#auth-form-bearer-token #hide-value-checkbox", Checkbox
            )

            # Uncheck then recheck
            checkbox.toggle()
            await pilot.pause()
            results["token_after_first_toggle"] = token_input.password

            checkbox.toggle()
            await pilot.pause()

            # Should be hidden again
            results["checkbox_final"] = checkbox.value
            results["token_final"] = token_input.password

        snap_compare(
            make_posting(collection=SAMPLE_COLLECTIONS),
            run_before=run_before,
            terminal_size=(80, 40),
        )
        assert results["token_after_first_toggle"] is False
        assert results["checkbox_final"] is True
        assert results["token_final"] is True

    def test_get_values_works_regardless_of_visibility(self, snap_compare):
        """get_values should work correctly whether token is hidden or visible."""
        results = {}

        async def run_before(pilot: Pilot):
            await pilot.press("ctrl+o", "t")  # jump to 'Auth' tab
            await pilot.pause()
            auth_select = pilot.app.query_one("#auth-type-select")
            auth_select.value = "bearer-token"
            await pilot.pause()

            form = pilot.app.query_one("#auth-form-bearer-token", BearerTokenForm)
            form.set_values("my-secret-token")

            # Test with hidden token
            values_hidden = form.get_values()
            results["token_hidden"] = values_hidden["token"]

            # Reveal token
            checkbox = pilot.app.query_one(
                "#auth-form-bearer-token #hide-value-checkbox", Checkbox
            )
            checkbox.toggle()
            await pilot.pause()

            # Test with visible token
            values_visible = form.get_values()
            results["token_visible"] = values_visible["token"]

        snap_compare(
            make_posting(collection=SAMPLE_COLLECTIONS),
            run_before=run_before,
            terminal_size=(80, 40),
        )
        assert results["token_hidden"] == "my-secret-token"
        assert results["token_visible"] == "my-secret-token"

    def test_validation_still_works_when_visible(self, snap_compare):
        """Validation should still work when the token is visible."""
        results = {}

        async def run_before(pilot: Pilot):
            await pilot.press("ctrl+o", "t")  # jump to 'Auth' tab
            await pilot.pause()
            auth_select = pilot.app.query_one("#auth-type-select")
            auth_select.value = "bearer-token"
            await pilot.pause()

            # Reveal token
            checkbox = pilot.app.query_one(
                "#auth-form-bearer-token #hide-value-checkbox", Checkbox
            )
            checkbox.toggle()
            await pilot.pause()

            token_input = pilot.app.query_one("#token-input", Input)

            # Empty token should show validation error
            token_input.value = ""
            token_input.validate(token_input.value)
            await pilot.pause()

            label = pilot.app.query_one("#token-empty-label", Label)
            results["label_visible_when_empty"] = label.visible

            # Non-empty token should hide validation error
            token_input.value = "valid-token"
            token_input.validate(token_input.value)
            await pilot.pause()

            results["label_visible_when_valid"] = label.visible

        snap_compare(
            make_posting(collection=SAMPLE_COLLECTIONS),
            run_before=run_before,
            terminal_size=(80, 40),
        )
        assert results["label_visible_when_empty"] is True
        assert results["label_visible_when_valid"] is False


@use_config("general.yaml")
class TestDigestAuthFormHideValue:
    """Tests for the Hide Value checkbox in Digest Auth (uses UserNamePasswordForm)."""

    def test_digest_auth_password_hidden_by_default(self, snap_compare):
        """Password input should be masked by default when Digest auth is selected."""
        results = {}

        async def run_before(pilot: Pilot):
            await pilot.press("ctrl+o", "t")  # jump to 'Auth' tab
            await pilot.pause()
            auth_select = pilot.app.query_one("#auth-type-select")
            auth_select.value = "digest"
            await pilot.pause()

            password_input = pilot.app.query_one("#password-input", Input)
            results["password_hidden"] = password_input.password

            checkbox = pilot.app.query_one(
                "#auth-form-digest #hide-value-checkbox", Checkbox
            )
            results["checkbox_checked"] = checkbox.value

        snap_compare(
            make_posting(collection=SAMPLE_COLLECTIONS),
            run_before=run_before,
            terminal_size=(80, 40),
        )
        assert results["password_hidden"] is True
        assert results["checkbox_checked"] is True

    def test_digest_auth_unchecking_reveals_password(self, snap_compare):
        """Unchecking Hide Value in Digest auth reveals the password."""
        results = {}

        async def run_before(pilot: Pilot):
            await pilot.press("ctrl+o", "t")  # jump to 'Auth' tab
            await pilot.pause()
            auth_select = pilot.app.query_one("#auth-type-select")
            auth_select.value = "digest"
            await pilot.pause()

            # Query within the digest form specifically
            digest_form = pilot.app.query_one("#auth-form-digest", UserNamePasswordForm)
            password_input = digest_form.query_one("#password-input", Input)
            checkbox = digest_form.query_one("#hide-value-checkbox", Checkbox)

            # Initially hidden
            results["initially_hidden"] = password_input.password

            # Toggle to reveal
            checkbox.toggle()
            await pilot.pause()

            # Now visible
            results["checkbox_after_toggle"] = checkbox.value
            results["password_after_toggle"] = password_input.password

        snap_compare(
            make_posting(collection=SAMPLE_COLLECTIONS),
            run_before=run_before,
            terminal_size=(80, 40),
        )
        assert results["initially_hidden"] is True
        assert results["checkbox_after_toggle"] is False
        assert results["password_after_toggle"] is False
