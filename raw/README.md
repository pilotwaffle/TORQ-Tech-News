# raw/ — Original Assets (Immutable)

This directory holds original, unaltered source material for the TORQ Tech News
knowledge base. Everything here is treated as **read-only ground truth**.

## The rule

**Nothing inside `raw/` is ever edited, reformatted, renamed, reorganized, or
deleted by an AI assistant.** Only the human owner adds, changes, or removes
files here.

Reason: the knowledge base is self-improving, which means its derived layers
(`wiki/`, notes, summaries) get rewritten freely and often. That is only safe if
there is a layer underneath that never drifts. `raw/` is that layer. If an AI
could "tidy" it, every regeneration would compound small distortions until the
originals no longer said what they originally said.

## What goes here

Original assets, exactly as received or authored:

- Documents, PDFs, exports, transcripts
- Screenshots, images, diagrams
- Data dumps, CSVs, JSON exports
- Reference material, saved articles, notes written by hand
- Anything you want preserved verbatim

## What does NOT go here

- AI-generated summaries or indexes — those belong in `wiki/`
- Live application code — it stays at the repo root (see `/CLAUDE.md`)
- Anything you expect an assistant to update in place

## Organizing

Use whatever subfolder structure you like. Create it yourself; an assistant will
not restructure it for you. `wiki/` adapts to however `raw/` is arranged, not
the other way around.

## Current state

Empty as of setup. Drop files in and ask for a wiki regeneration.
