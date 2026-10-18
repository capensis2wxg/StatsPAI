"""CI guard: ensures ``## For Agents`` blocks in docs guides are in
sync with the registry.

When registry metadata for a flagship family changes, the author
must re-run ``python scripts/sync_agent_blocks.py`` before committing
so the rendered guide matches the source of truth. This test runs
the script in --check mode and fails if drift is detected.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "sync_agent_blocks.py"


@pytest.mark.skipif(not SCRIPT.exists(), reason="sync script missing")
def test_agent_blocks_in_sync():
    """docs/guides/*.qmd ## For Agents blocks match the registry."""
    guides = sorted((REPO_ROOT / "docs" / "guides").glob("*.qmd"))
    marker_re = re.compile(r"<!--\s*AGENT-BLOCK-START:")
    localized_re = re.compile(
        r"<!--\s*AGENT-BLOCK-START:\s*[A-Za-z0-9_]+\s+locale=zh-CN\s*-->"
    )
    markers = [
        marker
        for guide in guides
        for marker in marker_re.findall(guide.read_text(encoding="utf-8"))
    ]
    localized_markers = [
        match
        for guide in guides
        for match in localized_re.findall(guide.read_text(encoding="utf-8"))
    ]
    assert len(markers) == len(localized_markers) > 0, (
        "Every agent block in the translated Quarto guides must be marked "
        "locale=zh-CN so generated English text cannot overwrite it."
    )

    res = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    if res.returncode != 0:
        msg = (
            "## For Agents blocks in docs are out of sync with the "
            "registry.\n\nRe-run:\n  python scripts/sync_agent_blocks.py\n\n"
            "Drift detected:\n" + res.stderr + "\n" + res.stdout
        )
        pytest.fail(msg)
