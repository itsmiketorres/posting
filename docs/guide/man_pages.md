## Overview

Posting includes man pages for quick reference in your terminal. Man pages provide offline documentation for the `posting` command and all its subcommands.

## Viewing Man Pages

To view the main Posting man page:

```bash
man posting
```

### Available Man Pages

| Page | Description |
|------|-------------|
| `man posting` | Main command overview and subcommand list |
| `man posting-default` | Default command (launches the TUI) |
| `man posting-import` | Import OpenAPI or Postman collections |
| `man posting-locate` | Find config, collection, and theme directories |
| `man posting-sponsors` | View project sponsors |

## Troubleshooting

### Man page not found

If you see `No manual entry for posting`, the man pages may not be in your system's search path.

**For pip installs:**

Add the installation prefix to your `MANPATH`:

```bash
# Find where posting is installed
python -c "import sys; print(sys.prefix)"

# Add to MANPATH (replace /path/to/prefix with the output above)
export MANPATH="/path/to/prefix/share/man:$MANPATH"
```

**For pipx installs:**

```bash
export MANPATH="$HOME/.local/share/man:$MANPATH"
```

Add this line to your shell config (`~/.bashrc`, `~/.zshrc`, etc.) to make it permanent.

**For virtual environment installs:**

Man pages are installed to `<venv>/share/man/man1/`. You can view them directly:

```bash
man .venv/share/man/man1/posting.1
```

Or add the venv's man directory to your `MANPATH`:

```bash
export MANPATH="$(pwd)/.venv/share/man:$MANPATH"
```

### Verifying installation

Check if the man page file exists:

```bash
# For system/pipx installs
ls ~/.local/share/man/man1/posting.1

# For venv installs
ls .venv/share/man/man1/posting.1
```

### Still having issues?

1. Reinstall Posting to ensure man pages are included
2. Check that `click-man` is installed as a dependency
3. Verify the wheel was built with man pages: `unzip -l posting*.whl | grep man`
