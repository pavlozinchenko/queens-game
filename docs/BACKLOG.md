# Backlog — queens-game

Not read at session start. Pulled from when `docs/PROJECT.md` → Next tasks has room. No size limit.

Order: first by *when* (the sections below), then by priority inside a section (H → M → L).
Priority meanings: `<kit>/playbook/06-priorities.md`.

## Next (first candidates for Next tasks)
- [M] (How to Play) 3-step illustrated example instead of a bullet list
- [M] (Win celebration) confetti or crown animation, max ~1.5 s, respects `prefers-reduced-motion`
- [M] (Hint) decide: highlight region vs single safe cell; count hints in results panel
- [L] (Themed levels) brainstorm 20 names/shapes; reuse generator with a seed mask
- [L] (General levels) 8 × 8x8 + 8 × 9x9 if 9x9 is approved (see Open questions)

## Later
- [M] Share-result button (copy emoji grid like Wordle)
- [L] Keyboard controls on desktop (arrows + space/enter)
- [L] Accessibility pass: focus rings, aria labels on cells, color-blind safe palette option

## Someday
- "Level of the day" chosen deterministically by date, still static

## Rejected (keep, with reason, so it is not proposed again)
- Difficulty labels: removed earlier, grid size is the only difficulty signal
- Translation keys per level (`translationKey`): directory-based matching is enough
