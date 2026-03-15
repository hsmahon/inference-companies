from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def expect(pattern: str, message: str, text: str, flags: int = re.MULTILINE | re.DOTALL) -> None:
    if not re.search(pattern, text, flags):
        fail(message)


def extract_css() -> str:
    match = re.search(r"<style>\s*(.*?)\s*</style>", HTML, re.DOTALL)
    if not match:
        fail("Expected an inline style block in index.html.")
    return match.group(1)


def block(selector: str, css: str) -> str:
    match = re.search(rf"{re.escape(selector)}\s*\{{(.*?)\}}", css, re.DOTALL)
    if not match:
        fail(f"Expected CSS block for {selector}.")
    return match.group(1)


css = extract_css()

expect(r"family=Azeret\+Mono", "Expected Azeret Mono to be the imported font family.", HTML)
font_families = re.findall(r"family=([^:&\"']+)", HTML)
if font_families != ["Azeret+Mono"]:
    fail(f"Expected exactly one imported font family, found: {font_families}")

expect(r"--font-mono:\s*\"Azeret Mono\"", "Expected :root to define the mono font token.", css)

for value in re.findall(r"font-family:\s*([^;]+);", css):
    if "var(--font-mono)" not in value and '"Azeret Mono"' not in value:
        fail(f"Unexpected font-family declaration: {value}")

h1 = block("h1", css)
for required in (
    "font-weight: 700",
    "font-size: clamp(2.65rem, 5vw, 4.85rem)",
    "letter-spacing: -.04em",
    "text-transform: uppercase",
):
    if required not in h1:
        fail(f"Expected h1 to include `{required}`.")

subtitle = block(".subtitle", css)
for required in (
    "font-size: 1rem",
    "line-height: 1.8",
    "max-width: 68ch",
):
    if required not in subtitle:
        fail(f"Expected .subtitle to include `{required}`.")

headers = block("th", css)
for required in (
    "font-size: .72rem",
    "letter-spacing: .14em",
    "font-weight: 600",
):
    if required not in headers:
        fail(f"Expected th to include `{required}`.")

body = block("body", css)
for required in (
    "font-family: var(--font-mono)",
    "text-rendering: optimizeLegibility",
    "font-variant-numeric: lining-nums tabular-nums",
):
    if required not in body:
        fail(f"Expected body to include `{required}`.")

print("Typography verification passed.")
