# TORQ Tech News — Project Rules

This repo holds two separate things. Do not mix them.

1. **A live production web app** at the root (Flask + static, deployed via
   Vercel / Railway / GitHub Actions).
2. **A knowledge base layer** in `raw/` and `wiki/`.

---

## Knowledge base rules (binding, every session)

### `raw/` — original assets, add-only

- **Adding new files is allowed. Existing files are immutable.**
- **Never edit, reformat, rename, move, reorganize, or delete anything already in
  `raw/`** — however messy, duplicated, or badly named it looks. Add-only is not
  permission to tidy. Do not propose restructuring it.
- Why: `wiki/` is regenerated destructively. That is only safe when the layer
  beneath it never drifts. `raw/` is the ground truth.

### `wiki/` — AI-written, never hand-edited

- Everything in `wiki/` is written and rewritten by an AI assistant. Treat any
  file there as disposable and regenerable.
- The wiki **references** `raw/`; it does not duplicate it. Link to paths, do not
  paste asset contents in wholesale.
- **Verify every path before writing it.** Only link to files confirmed to exist
  by an actual directory read this session. Never write a remembered or inferred
  path.
- Describe what an asset actually contains, not what its filename suggests. If
  the purpose is unclear, list it under Gaps rather than guessing.
- On "regenerate the wiki": re-scan `raw/`, rewrite `wiki/INDEX.md`, drop stale
  entries. Do not touch `raw/` in the process.

### Automation

- A global `SessionStart` hook (`~/.claude/hooks/kb-scan.py`) reports which
  `raw/` assets are not yet referenced by `wiki/`. It is read-only.
- When it reports unindexed assets, **tell the user and offer to regenerate**.
  Never regenerate `wiki/` unprompted.
- To capture files: `python ~/.claude/hooks/kb-capture.py <paths> [--into SUBDIR]`.
  Use `--dry-run` first when capturing a directory.

---

## Application code rules

- All app code, assets, and deploy config stay at the repository root. Do **not**
  move them into `raw/`, `wiki/`, or any new folder.
- `vercel.json`, `Procfile`, `railway.*`, `Dockerfile`, `start.sh`, and
  `.github/workflows/` resolve paths from the repo root. Moving or renaming root
  files breaks production deploys.

---

## Boundary

`raw/` and `wiki/` are not part of the deployed application. The application is
not part of the knowledge base. Restructuring proposals that cross this line
require explicit user sign-off before any file is touched.
