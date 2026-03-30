# Queens Game

A web-based puzzle game inspired by LinkedIn's Queens mini-game. Place queens on a colored grid so that no two queens share the same row, column, or are diagonally adjacent.

## How to Play

- The board is divided into colored regions
- Place exactly **one queen** in each colored region
- No two queens can be in the **same row** or **column**
- No two queens can be **adjacent** (including diagonally)
- **Desktop:** left click to place a cross (mark), right click to place a queen
- **Mobile:** tap to cycle: cross, queen, clear

## Features

- 15 levels: Easy (4-5), Medium (6-7), Hard (8-8)
- Dark/light theme with toggle
- English/Ukrainian localization (Hugo i18n)
- Timer and move counter (can be hidden in settings)
- Undo/restart, prev/next level navigation
- General and themed level categories
- Unique solution guaranteed for every level

## Tech Stack

- [Hugo](https://gohugo.io/) — static site generator
- Vanilla JS — game logic
- CSS — styling, no frameworks
- Python — level generator script

## Project Structure

```
content/
  en/                    # English content
    general/             # General levels (numbered)
    themed/              # Themed levels (named)
  uk/                    # Ukrainian content (same structure)
i18n/                    # Translation files (en.toml, uk.toml)
layouts/                 # Hugo templates
  levels/single.html     # Level page template
  index.html             # Level selector with tabs
assets/css/style.css     # All styles
static/js/game.js        # Game logic
scripts/
  generate_levels.py     # Level generator
  save_level.py          # Save generated level to content files
```

## Level Generation

```bash
# Generate a level and save it
python3 scripts/generate_levels.py easy | python3 scripts/save_level.py --level 1
python3 scripts/generate_levels.py medium | python3 scripts/save_level.py --level 6
python3 scripts/generate_levels.py --size 8 | python3 scripts/save_level.py --level 11

# Overwrite existing level
python3 scripts/generate_levels.py easy | python3 scripts/save_level.py --level 1 --force
```

## Development

```bash
hugo server
```

## Deploy

Built for Cloudflare Pages. Build command: `hugo`, output directory: `public`.

## Author

Made by [Pavlo Zinchenko](https://justpavlo.me)
