from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_readme_markdown_matches_quarto_source():
    assert (REPO_ROOT / "README.md").read_bytes() == (
        REPO_ROOT / "README.qmd"
    ).read_bytes()
