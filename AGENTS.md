# AGENTS.md — queens-game

Kind: **product**. A browser puzzle game: both code (game logic, level generator) and content (levels, texts, layout). Public repo (MIT), deployed to Cloudflare Pages.

## Start here
Read `docs/PROJECT.md` and the newest `docs/journal/*.md` before doing anything. Follow the session workflow described in `docs/PROJECT.md` → "Process".

## Project specifics
- Stack: Hugo (multilingual, `content/{en,uk}`), vanilla JS in `static/js/game.js`, CSS in 5 modules under `assets/css/` concatenated by Hugo Pipes. Python level generator in `scripts/`. No frameworks, no server side.
- Run: `hugo server`. Build check: `hugo` (output `public/`, git-ignored). Deploy is automatic from `main` via Cloudflare Pages.
- Levels: `content/{en,uk}/general/level-N.md` (sizes 4x4→8x8) and `content/{en,uk}/themed/<name>.md`. Every level must have exactly one solution; the generator enforces this (`fix_uniqueness`). Generate one level at a time and show it for visual approval before saving.
  `python3 scripts/generate_levels.py --size 6 | python3 scripts/save_level.py --level 13` (`--force` to overwrite).
- Both languages must stay in sync: a level or i18n key added in `en` is added in `uk` in the same step. No unused i18n keys.
- Input model: `pointerup` + `pointerType === "touch"` splits desktop/mobile; do not reintroduce click/touchstart handlers.
- Progress is stored in localStorage with cookie fallback (Telegram WebView); keep both paths working.
- Verify on mobile viewports (Chrome, Firefox, Telegram WebView) for anything touching the board, buttons or zoom.
- Conventional commits (`feat:`, `fix:`), English.

## Forbidden without asking
- Changing level numbering or URLs of existing levels (breaks saved progress and links).
- Removing or regenerating an existing level.
- Adding a build dependency or a JS framework.

## Tools
None beyond Hugo and Python 3.

## Rules
- Every change ships with its verification: a `hugo` build, a browser check on a phone-sized viewport, or a test; note it in the journal.
- Name which layer a task touches: game logic, level data, text/i18n, or presentation (layout, styling). Do not mix them in one step.
- No magic numbers, no dead code, no duplicated logic, no unused i18n keys.
- Prefer the smallest diff that solves the task. Refactors are separate, approved steps.
- Dependencies: none today; adding one is an ADR.
- Verification for texts means re-reading as a casual player on a phone seeing the game for the first time.
- Visual standard: minimal, pixel-aligned, consistent spacing, equal button sizes, readable contrast, SVG icons only.
- Strict formats: ISO-8601 dates.
- URL, title or structure changes to published pages get an ADR (hard to undo).
