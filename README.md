# Queens Game

A web-based puzzle game inspired by LinkedIn's Queens mini-game. Place queens on a colored grid so that no two queens share the same row, column, or are diagonally adjacent.

## How to Play

- The board is divided into colored regions
- Place exactly **one queen** in each colored region
- No two queens can be in the **same row** or **column**
- No two queens can be **adjacent** (including diagonally)
- **Desktop:** left click — cross (mark), right click — queen
- **Mobile:** tap to cycle: cross → queen → clear

## Features

- 36 general levels (4x4 → 8x8) + themed levels
- Dark/light theme
- English/Ukrainian localization
- Timer and move counter (hideable in settings)
- Progress tracking — best time and moves saved per level
- Undo/restart, prev/next/random level navigation
- Every level has a unique solution

## Tech Stack

- [Hugo](https://gohugo.io/) — static site generator
- Vanilla JS — game logic
- CSS (5 modules via Hugo Pipes) — styling, no frameworks
- Python — level generator

## Project Structure

```
content/{en,uk}/
  general/             # General levels (numbered)
  themed/              # Themed levels (named)
i18n/                  # Translations (en.toml, uk.toml)
layouts/
  levels/single.html   # Level page template
  index.html           # Level selector with tabs
assets/css/
  variables.css        # Themes and CSS custom properties
  base.css             # Reset, buttons, overlays
  layout.css           # Header, footer, toggles
  levels.css           # Level selector, cards, progress
  game.css             # Board, cells, modals
static/js/game.js      # Game logic
scripts/
  generate_levels.py   # Level generator
  save_level.py        # Save generated level to content files
```

## Level Generation

```bash
# Generate and save a level
python3 scripts/generate_levels.py --size 5 | python3 scripts/save_level.py --level 1
python3 scripts/generate_levels.py --size 8 | python3 scripts/save_level.py --level 30

# Overwrite existing
python3 scripts/generate_levels.py --size 7 | python3 scripts/save_level.py --level 21 --force
```

## Development

```bash
hugo server
```

## Deploy

Cloudflare Pages. Build command: `hugo`, output directory: `public`.

## Contributing

Contributions are welcome! Feel free to open a PR with new levels, bug fixes, or improvements.

## License

[MIT](LICENSE)

## Author

Made by [Pavlo Zinchenko](https://justpavlo.me)
