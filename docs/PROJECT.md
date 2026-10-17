# queens-game

| Field | Value |
|-------|-------|
| Kind | product |
| Stage | maintained |

## Goal
A free, fast, no-account browser version of the LinkedIn "Queens" puzzle: colored regions, one queen per region/row/column, no adjacent queens. Works well on a phone, in EN and UK, with saved progress.

## Non-goals
- No accounts, backend, ads or analytics beyond what Cloudflare gives for free.
- No daily-puzzle feed or multiplayer.
- No frameworks; it stays Hugo + vanilla JS + CSS.

## Finish line
Healthy when:
- `hugo` builds clean and the site is live on Cloudflare Pages.
- Every level has exactly one solution and exists in both `en` and `uk`.
- Board, buttons and progress work on mobile Chrome, Firefox and Telegram WebView.
- No unused i18n keys; both languages render every string.

## Status (2026-10-17)
Live and stable: 36 general + 5 themed levels, EN/UK, dark/light theme, timer, undo, saved progress with cookie fallback. Last code change 2026-04-01. Adopted into the playbook today; `hugo` builds clean; no task started.

## Next tasks
| Task | Done when | Priority | Status | Updated |
|------|-----------|----------|--------|---------|
| Commit the adoption | `AGENTS.md`, `CLAUDE.md`, `docs/`, `.gitignore` committed | H | planned | 2026-10-17 |
| Clearer "How to Play" | rules page rewritten and understood by a first-time player | H | planned | 2026-10-17 |
| Win celebration | win modal replaced by a short celebration that works on mobile | M | planned | 2026-10-17 |
| Hint button | hint highlights a safe cell or region, with a counter, in both languages | M | planned | 2026-10-17 |
| More themed levels | +20 themed levels, each visually approved | M | planned | 2026-10-17 |
| More general levels | +16 general levels (sizes 6–9), each visually approved | L | planned | 2026-10-17 |

Other tasks: `docs/BACKLOG.md`.

## Open questions
- (2026-10-17) Extend general levels to 9x9, or stay at 8x8 max?
- (2026-10-17) Hint: highlight a whole region, or a single safe cell?
- (2026-10-17) Win celebration: animation only, or sound too?

Other questions: `docs/QUESTIONS.md`.

## How to resume
Read this file, then `docs/journal/` newest entry, then `AGENTS.md`. Run the `start-session` skill.

## Process
This product follows the personal playbook (`~/Claude/playbook/`): sessions start by reading this file, work in small approved steps, and end by updating **Status** and **Next tasks** and adding a journal entry. Decisions go to `docs/decisions/`.
