# wiki/ — AI-Written Index (Do Not Hand-Edit)

Derived layer of the TORQ Tech News knowledge base. Every file here is written
and rewritten by an AI assistant. It is a table of contents and navigation layer
that **references** files in `raw/` — it does not replace or duplicate them.

## The rule

**Hand edits are not preserved.** Any file in `wiki/` may be regenerated in full
at any time, which overwrites manual changes without warning. If you want
something to persist, put it in `raw/` and the wiki will reference it.

## What lives here

- `INDEX.md` — the master table of contents for `raw/`
- Topic pages that group related `raw/` assets and explain how they connect
- Cross-reference and gap notes

## Contract for generated pages

Every entry must:

1. Link to a real, verified path under `raw/` — never a guessed or remembered one
2. Describe what the asset actually contains, not what its filename implies
3. Say what is unknown rather than inferring it
4. Never restate the asset's content as if it were the asset (the wiki points; it
   does not replace)

## Regenerating

Ask: "regenerate the wiki." The assistant re-scans `raw/`, verifies every path,
and rewrites this directory. Stale entries pointing at removed files are dropped.

## Current state

`raw/` is empty, so `INDEX.md` has no entries yet.
