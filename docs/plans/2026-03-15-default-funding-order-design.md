# Default Funding Order Design

**Date:** 2026-03-15

## Goal

Make the default visible order of companies sort by funding round from `Seed` upward through the series ladder, with `Public` entries at the end.

## Context

The page already supports column sorting and already defines a funding-tier map in JavaScript. The current default view depends on raw HTML row order, which means the table opens in a mixed sequence instead of the intended fundraising progression.

## Chosen Direction

Keep the HTML rows editable in any source order and sort the table on page load using the existing funding-tier logic. This avoids maintaining two sources of truth and ensures future additions automatically land in the correct default order.

## Scope

- Reuse the current `TIER` ordering map.
- Apply ascending sort on the `Funding Round` column during initialization.
- Keep click-to-sort behavior working after page load.
- Show the current sort state in the funding-round header.

## Non-Goals

- No manual row reordering in HTML
- No new controls or filters
- No changes to the visual layout beyond sort-state feedback

## Verification

Add a regression script that renders the page headlessly, reads the post-JavaScript DOM, and confirms:

- funding-round values are nondecreasing from `seed` upward
- `public` rows appear at the end
- the `Funding Round` header displays ascending sort state
