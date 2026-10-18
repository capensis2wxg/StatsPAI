"""Docs are authored as Quarto (``.qmd``); only tool-mandated ``.md`` stay.

The MkDocs → Quarto migration left one class of files that must stay
Markdown, because outside tooling hard-codes the filename:

* ``README.md`` — ``pyproject.toml`` declares ``readme = "README.md"``
  (PyPI / sdist), and GitHub only renders ``README.md`` as the repository
  landing page.  It is a generated copy: edit ``README.qmd`` and run
  ``python scripts/sync_readme.py`` (guarded by
  ``tests/test_readme_qmd_sync.py``).
* ``paper.md`` — the JOSS (openjournals) submission format, paired with
  ``paper.bib``.  ``.qmd`` is not accepted.
* ``rust/statspai_hdfe/README.md`` — ``Cargo.toml`` declares
  ``readme = "README.md"`` (crates.io); Cargo resolves that path literally.

Any other ``.md`` file is a leftover of the migration and should be
converted to ``.qmd`` (or deleted if it was superseded).
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ALLOWED_MARKDOWN = {
    "README.md",
    "paper.md",
    "rust/statspai_hdfe/README.md",
}

# Directories that never hold authored docs: VCS/caches/build output.
SKIP_DIRS = {
    ".git",
    ".codebuddy",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".quarto",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "_site",
    "_freeze",
    "build",
    "dist",
    ".benchmarks",
}


def _iter_markdown(root: Path):
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts[:-1]):
            continue
        # Skip anything git itself ignores (e.g. *.egg-info, .pytest_cache).
        yield path.relative_to(root).as_posix()


def test_only_allowlisted_markdown_files_exist():
    stray = sorted(set(_iter_markdown(REPO_ROOT)) - ALLOWED_MARKDOWN)
    assert not stray, (
        "Unexpected Markdown file(s) found. Docs must be authored as .qmd; "
        "convert or delete them (see the module docstring for the four "
        "tool-mandated exceptions):\n  - " + "\n  - ".join(stray)
    )


def test_allowlisted_markdown_files_still_exist():
    missing = sorted(
        name for name in ALLOWED_MARKDOWN
        if not (REPO_ROOT / name).exists()
    )
    assert not missing, (
        "Tool-mandated Markdown copy missing (external tooling breaks "
        "without it):\n  - " + "\n  - ".join(missing)
    )
