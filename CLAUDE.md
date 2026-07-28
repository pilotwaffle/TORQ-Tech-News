# TORQ Tech News — Project Rules

This repo holds two separate things. Do not mix them.

1. **A live production web app** at the repository root (Flask + static site,
   deployed via Vercel / Railway / GitHub Actions).
2. **A knowledge base layer** in `raw/` and `wiki/`.

---

## Knowledge base rules (binding, every session)

### `raw/` — original assets, immutable

- **Never edit, reformat, rename, move, reorganize, or delete anything in `raw/`.**
  This holds regardless of how messy, duplicated, or badly named it looks.
- Read from `raw/` freely. Write to it only when the user explicitly asks to add
  a specific file.
- Do not "clean up" `raw/`. Do not propose restructuring it. Do not create
  subfolders in it uninvited.
- Why: `wiki/` is regenerated destructively. That is only safe when the layer
  beneath it never drifts. `raw/` is the immutable ground truth.

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
- If the user hand-edits `wiki/`, tell them it will be lost on regeneration and
  offer to move the content to `raw/` instead.

---

## Application code rules

- All app code, assets, and deploy config stay at the repository root. Do **not**
  move them into `raw/`, `wiki/`, or any new folder.
- `vercel.json`, `Procfile`, `railway.json`, `railway.toml`, `Dockerfile`,
  `start.sh`, and `.github/workflows/` resolve paths from the repo root.
  Moving or renaming root files breaks production deploys.
- Never route app code through the knowledge base, or knowledge base files into
  the deploy path.

---

## Boundary

`raw/` and `wiki/` are not part of the deployed application. The application is
not part of the knowledge base. Restructuring proposals that cross this line
require explicit user sign-off before any file is touched.
