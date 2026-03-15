from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "index.html"
EDGE_CANDIDATES = (
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
)
TIER = {"seed": 0, "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "public": 8, "strategic": 9, "other": 10}


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def edge_path() -> Path:
    for candidate in EDGE_CANDIDATES:
        if candidate.exists():
            return candidate
    fail("Microsoft Edge was not found in the expected locations.")


def dump_dom() -> str:
    command = [
        str(edge_path()),
        "--headless=new",
        "--disable-gpu",
        "--dump-dom",
        PAGE.as_uri(),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        fail(f"Headless Edge failed with exit code {result.returncode}: {result.stderr.strip()}")
    return result.stdout


dom = dump_dom()
rounds = re.findall(r'<td data-label="Funding Round" data-val="([^"]+)"', dom)
if not rounds:
    fail("Could not extract funding-round cells from the rendered DOM.")

actual = [value.lower() for value in rounds]
expected = sorted(actual, key=lambda value: TIER.get(value, 99))
if actual != expected:
    fail(f"Expected funding rounds in ascending default order, found: {actual}")

header_block_match = re.search(r'(<th[^>]*data-col="2"[^>]*>.*?</th>)', dom, re.DOTALL)
if not header_block_match:
    fail("Expected to find the Funding Round header in the rendered DOM.")

header_block = header_block_match.group(1)
header_match = re.search(r'class="([^"]*)"', header_block)
if not header_match or "sort-asc" not in header_match.group(1):
    fail("Expected the Funding Round header to show ascending sort state on load.")

arrow_match = re.search(r'<span class="sort-arrow">([^<]+)</span>', header_block)
if not arrow_match:
    fail("Expected the Funding Round header to include a sort arrow.")

print("Default funding-order verification passed.")
