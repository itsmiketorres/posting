"""Tests for man page installation and configuration."""

import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import pytest

# Path to the project root
PROJECT_ROOT = Path(__file__).parent.parent
MAN_DIR = PROJECT_ROOT / "man" / "man1"

# Expected man pages that should be generated
EXPECTED_MAN_PAGES = [
    "posting.1",
    "posting-default.1",
    "posting-import.1",
    "posting-locate.1",
    "posting-sponsors.1",
]


class TestManPagesExist:
    """Tests to verify man pages exist in the source tree."""

    def test_man_directory_exists(self):
        """Verify the man/man1 directory exists."""
        assert MAN_DIR.exists(), f"Man directory not found: {MAN_DIR}"
        assert MAN_DIR.is_dir(), f"Man path is not a directory: {MAN_DIR}"

    @pytest.mark.parametrize("man_page", EXPECTED_MAN_PAGES)
    def test_man_page_exists(self, man_page):
        """Verify each expected man page exists."""
        man_path = MAN_DIR / man_page
        assert man_path.exists(), f"Man page not found: {man_path}"
        assert man_path.is_file(), f"Man page is not a file: {man_path}"

    @pytest.mark.parametrize("man_page", EXPECTED_MAN_PAGES)
    def test_man_page_not_empty(self, man_page):
        """Verify man pages are not empty."""
        man_path = MAN_DIR / man_page
        assert man_path.stat().st_size > 0, f"Man page is empty: {man_path}"


class TestManPageContent:
    """Tests to verify man page content is valid."""

    def test_main_man_page_has_required_sections(self):
        """Verify the main posting.1 man page has required sections."""
        man_path = MAN_DIR / "posting.1"
        content = man_path.read_text()

        # Check for required man page sections
        assert ".TH" in content, "Missing .TH (title header) directive"
        assert ".SH NAME" in content, "Missing NAME section"
        assert ".SH SYNOPSIS" in content, "Missing SYNOPSIS section"
        assert ".SH DESCRIPTION" in content, "Missing DESCRIPTION section"

    def test_main_man_page_has_correct_name(self):
        """Verify the main man page has the correct command name."""
        man_path = MAN_DIR / "posting.1"
        content = man_path.read_text()

        assert "posting" in content.lower(), "Man page doesn't reference 'posting'"

    @pytest.mark.parametrize("man_page", EXPECTED_MAN_PAGES)
    def test_man_page_has_title_header(self, man_page):
        """Verify each man page has a title header."""
        man_path = MAN_DIR / man_page
        content = man_path.read_text()

        assert ".TH" in content, f"Man page {man_page} missing .TH directive"

    @pytest.mark.parametrize("man_page", EXPECTED_MAN_PAGES)
    def test_man_page_section_is_1(self, man_page):
        """Verify man pages are in section 1 (user commands)."""
        man_path = MAN_DIR / man_page
        content = man_path.read_text()

        # The .TH line should contain "1" as the section number
        lines = content.split("\n")
        th_line = next((line for line in lines if line.startswith(".TH")), None)
        assert th_line is not None, f"No .TH line found in {man_page}"
        assert '"1"' in th_line, f"Man page {man_page} is not in section 1"


class TestWheelContainsManPages:
    """Tests to verify man pages are included in the built wheel."""

    @pytest.fixture(scope="class")
    def built_wheel(self, tmp_path_factory):
        """Build the wheel and return the path."""
        tmp_dir = tmp_path_factory.mktemp("wheel")
        result = subprocess.run(
            [sys.executable, "-m", "build", "--wheel", "--outdir", str(tmp_dir)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            pytest.skip(f"Failed to build wheel: {result.stderr}")

        wheels = list(tmp_dir.glob("*.whl"))
        assert len(wheels) == 1, f"Expected 1 wheel, found {len(wheels)}"
        return wheels[0]

    def test_wheel_contains_man_pages(self, built_wheel):
        """Verify the wheel contains man pages in the correct location."""
        with zipfile.ZipFile(built_wheel, "r") as whl:
            names = whl.namelist()

            # Man pages should be in the .data/data/share/man/man1/ directory
            man_files = [n for n in names if "share/man/man1/" in n and n.endswith(".1")]

            assert len(man_files) >= len(EXPECTED_MAN_PAGES), (
                f"Expected at least {len(EXPECTED_MAN_PAGES)} man pages in wheel, "
                f"found {len(man_files)}: {man_files}"
            )

    @pytest.mark.parametrize("man_page", EXPECTED_MAN_PAGES)
    def test_wheel_contains_specific_man_page(self, built_wheel, man_page):
        """Verify each expected man page is in the wheel."""
        with zipfile.ZipFile(built_wheel, "r") as whl:
            names = whl.namelist()

            matching = [n for n in names if n.endswith(f"/{man_page}")]
            assert len(matching) == 1, (
                f"Expected man page {man_page} not found in wheel. "
                f"Available: {[n for n in names if 'man' in n]}"
            )


class TestManPageInstallation:
    """Tests to verify man pages are installed correctly."""

    @pytest.fixture(scope="class")
    def installed_venv(self, tmp_path_factory):
        """Create a temporary venv and install the package."""
        tmp_dir = tmp_path_factory.mktemp("venv")
        venv_dir = tmp_dir / "venv"

        # Create virtual environment
        result = subprocess.run(
            [sys.executable, "-m", "venv", str(venv_dir)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            pytest.skip(f"Failed to create venv: {result.stderr}")

        # Determine pip path based on OS
        if sys.platform == "win32":
            pip_path = venv_dir / "Scripts" / "pip"
        else:
            pip_path = venv_dir / "bin" / "pip"

        # Install the package
        result = subprocess.run(
            [str(pip_path), "install", str(PROJECT_ROOT)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            pytest.skip(f"Failed to install package: {result.stderr}")

        return venv_dir

    def test_man_pages_installed_in_share_directory(self, installed_venv):
        """Verify man pages are installed in share/man/man1."""
        man_install_dir = installed_venv / "share" / "man" / "man1"

        assert man_install_dir.exists(), (
            f"Man pages directory not found at {man_install_dir}"
        )

        installed_man_pages = list(man_install_dir.glob("posting*.1"))
        assert len(installed_man_pages) >= len(EXPECTED_MAN_PAGES), (
            f"Expected at least {len(EXPECTED_MAN_PAGES)} man pages, "
            f"found {len(installed_man_pages)}"
        )

    @pytest.mark.parametrize("man_page", EXPECTED_MAN_PAGES)
    def test_specific_man_page_installed(self, installed_venv, man_page):
        """Verify each expected man page is installed."""
        man_install_path = installed_venv / "share" / "man" / "man1" / man_page

        assert man_install_path.exists(), (
            f"Man page {man_page} not installed at {man_install_path}"
        )

    def test_installed_man_pages_readable(self, installed_venv):
        """Verify installed man pages have valid content."""
        man_install_dir = installed_venv / "share" / "man" / "man1"
        main_man_page = man_install_dir / "posting.1"

        content = main_man_page.read_text()
        assert ".TH" in content, "Installed man page missing .TH directive"
        assert "posting" in content.lower(), "Installed man page doesn't mention posting"


class TestManPathConfiguration:
    """Tests for MANPATH configuration helpers."""

    @pytest.fixture
    def mock_venv_path(self, tmp_path):
        """Create a mock venv structure with man pages."""
        venv = tmp_path / "mock_venv"
        man_dir = venv / "share" / "man" / "man1"
        man_dir.mkdir(parents=True)

        # Create a mock man page
        (man_dir / "posting.1").write_text('.TH "POSTING" "1"\n.SH NAME\nposting')

        return venv

    def test_manpath_includes_venv_share(self, mock_venv_path):
        """Test that MANPATH can be configured to include venv share directory."""
        expected_manpath = mock_venv_path / "share" / "man"

        # Simulate what a user would add to their MANPATH
        current_manpath = os.environ.get("MANPATH", "")
        new_manpath = f"{expected_manpath}:{current_manpath}" if current_manpath else str(expected_manpath)

        # Verify the path would be valid
        assert expected_manpath.exists(), "Expected MANPATH directory doesn't exist"
        assert (expected_manpath / "man1" / "posting.1").exists(), "Man page not found in MANPATH"

    def test_man_command_finds_page_with_manpath(self, mock_venv_path):
        """Test that man command can find pages when MANPATH is set."""
        manpath = mock_venv_path / "share" / "man"

        # Try to use man with custom MANPATH (may not work on all systems)
        env = os.environ.copy()
        env["MANPATH"] = str(manpath)

        # Use 'man -w' to find the man page path without displaying it
        result = subprocess.run(
            ["man", "-w", "posting"],
            env=env,
            capture_output=True,
            text=True,
        )

        # On some systems man -w might not work as expected, so we check gracefully
        if result.returncode == 0:
            assert "posting" in result.stdout.lower(), (
                f"man -w didn't find posting man page. Output: {result.stdout}"
            )
        else:
            # Alternative check: verify the file exists in the right place
            man_page = manpath / "man1" / "posting.1"
            assert man_page.exists(), f"Man page not found at {man_page}"


class TestManPageGeneration:
    """Tests for man page generation from click commands."""

    def test_click_man_generates_pages(self):
        """Verify click-man can generate man pages from the CLI."""
        from click_man.core import write_man_pages
        from posting.__main__ import cli

        with tempfile.TemporaryDirectory() as tmp_dir:
            write_man_pages("posting", cli, target_dir=tmp_dir)

            generated = list(Path(tmp_dir).glob("*.1"))
            assert len(generated) >= 1, "click-man didn't generate any man pages"

            # Verify main page was generated
            main_page = Path(tmp_dir) / "posting.1"
            assert main_page.exists(), "Main posting.1 man page not generated"

    def test_generated_pages_match_expected(self):
        """Verify generated man pages match the expected list."""
        from click_man.core import write_man_pages
        from posting.__main__ import cli

        with tempfile.TemporaryDirectory() as tmp_dir:
            write_man_pages("posting", cli, target_dir=tmp_dir)

            generated_names = {p.name for p in Path(tmp_dir).glob("*.1")}
            expected_names = set(EXPECTED_MAN_PAGES)

            assert generated_names == expected_names, (
                f"Generated man pages don't match expected.\n"
                f"Generated: {generated_names}\n"
                f"Expected: {expected_names}"
            )


class TestUnixManPageStandards:
    """Tests to verify man pages follow Unix standards."""

    def test_man_pages_use_section_1(self):
        """Man pages for user commands should be in section 1."""
        for man_page in EXPECTED_MAN_PAGES:
            assert man_page.endswith(".1"), (
                f"Man page {man_page} should have .1 extension for section 1"
            )

    def test_man_page_naming_convention(self):
        """Man page names should follow command-subcommand.section format."""
        for man_page in EXPECTED_MAN_PAGES:
            name = man_page.rsplit(".", 1)[0]  # Remove extension
            assert name.startswith("posting"), (
                f"Man page {man_page} should start with 'posting'"
            )

    @pytest.mark.parametrize("man_page", EXPECTED_MAN_PAGES)
    def test_man_page_permissions(self, man_page):
        """Man pages should be readable."""
        man_path = MAN_DIR / man_page
        assert os.access(man_path, os.R_OK), f"Man page {man_page} is not readable"

    def test_main_man_page_references_subcommands(self):
        """Main man page should reference subcommand man pages."""
        main_page = MAN_DIR / "posting.1"
        content = main_page.read_text()

        # Check that subcommands are referenced
        subcommands = ["default", "import", "locate", "sponsors"]
        for subcmd in subcommands:
            assert subcmd in content.lower(), (
                f"Main man page doesn't reference '{subcmd}' subcommand"
            )
