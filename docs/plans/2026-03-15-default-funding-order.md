# Default Funding Order Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the table load sorted by funding round from `Seed` through the series progression, with `Public` companies at the end.

**Architecture:** Add a lightweight Python verification script that renders the local page with headless Edge and inspects the final DOM after JavaScript runs. Then refactor the inline table-sorting logic in `index.html` so the existing tier comparator is reused for both initial load and header clicks.

**Tech Stack:** HTML, inline CSS, vanilla JavaScript, Python via `uv`, Microsoft Edge headless

---

### Task 1: Add default-order regression coverage

**Files:**
- Create: `tests/verify_default_funding_order.py`
- Test: `tests/verify_default_funding_order.py`

**Step 1: Write the failing test**

Create a Python script that:

- launches the local `index.html` with headless Edge
- captures the final DOM with `--dump-dom`
- extracts each funding-round `data-val` from the rendered table body
- asserts the sequence is sorted by the page's tier ordering
- asserts the funding-round header includes the ascending sort state

**Step 2: Run test to verify it fails**

Run: `uv run python tests/verify_default_funding_order.py`
Expected: FAIL because the current page loads in raw HTML order, not funding-round order.

### Task 2: Implement on-load funding sorting

**Files:**
- Modify: `index.html`
- Test: `tests/verify_default_funding_order.py`
- Test: `tests/verify_typography.py`

**Step 1: Write minimal implementation**

Refactor the inline sorting code to:

- centralize row sorting in a reusable function
- centralize sort-indicator updates in a reusable function
- initialize the table to `Funding Round` ascending on page load
- preserve click toggling for all headers

**Step 2: Run tests to verify they pass**

Run: `uv run python tests/verify_default_funding_order.py`
Expected: PASS

Run: `uv run python tests/verify_typography.py`
Expected: PASS

### Task 3: Final verification

**Files:**
- Verify: `index.html`
- Verify: `tests/verify_default_funding_order.py`
- Verify: `tests/verify_typography.py`

**Step 1: Run final verification**

Run: `uv run python tests/verify_default_funding_order.py`
Expected: PASS

Run: `uv run python tests/verify_typography.py`
Expected: PASS

**Step 2: Review git state**

Run: `git status --short --branch`
Expected: modified `index.html` and new docs/tests only
