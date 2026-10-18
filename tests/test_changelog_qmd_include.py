"""The published changelog page embeds the single root CHANGELOG.qmd.

``docs/changelog.qmd`` used to be a stub pointing at GitHub, so the
rendered site never carried the release history and readers had to leave
the docs to find it.  It now includes the root file directly, which means
the root file is the only place a release entry may be added.

This guard fails if the include is dropped (or replaced by a hand-copied
snapshot, which would silently drift from the root file).
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ROOT_CHANGELOG = REPO_ROOT / "CHANGELOG.qmd"
DOCS_CHANGELOG = REPO_ROOT / "docs" / "changelog.qmd"
INCLUDE_DIRECTIVE = "{{< include ../CHANGELOG.qmd >}}"


def test_root_changelog_is_the_quarto_source():
    assert ROOT_CHANGELOG.exists(), (
        "CHANGELOG.qmd is missing; docs/changelog.qmd has nothing to include."
    )


def test_docs_changelog_includes_root_file():
    text = DOCS_CHANGELOG.read_text(encoding="utf-8")
    assert INCLUDE_DIRECTIVE in text, (
        "docs/changelog.qmd must embed the root changelog with "
        f"{INCLUDE_DIRECTIVE!r} instead of keeping a separate copy."
    )
