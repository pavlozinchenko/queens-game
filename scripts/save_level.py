#!/usr/bin/env python3
"""
Save a generated level grid to content files.

Usage:
  python generate_levels.py easy | python save_level.py --level 6
  python generate_levels.py --size 8 | python save_level.py --level 12 --category themed
  python generate_levels.py easy | python save_level.py --level 1 --force
"""

import argparse
import os
import sys

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "content")


def main():
    parser = argparse.ArgumentParser(description="Save level grid to content files")
    parser.add_argument("--level", type=int, required=True, help="Level number")
    parser.add_argument("--category", default="general",
                        help="Category directory (default: general)")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing level")
    args = parser.parse_args()

    grid = sys.stdin.read().strip()
    if not grid:
        print("Error: no grid data on stdin", file=sys.stderr)
        sys.exit(1)

    rows = grid.split("\n")
    grid_size = len(rows)

    content = "\n".join([
        "---",
        f'title: "Level {args.level}"',
        f"level: {args.level}",
        f"gridSize: {grid_size}",
        "---",
        grid,
        "",
    ])

    for lang in ["en", "uk"]:
        dirpath = os.path.join(CONTENT_DIR, lang, args.category)
        filepath = os.path.join(dirpath, f"level-{args.level}.md")

        if os.path.exists(filepath) and not args.force:
            print(f"Error: {filepath} already exists (use --force to overwrite)",
                  file=sys.stderr)
            sys.exit(1)

        os.makedirs(dirpath, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(content)

    print(f"Saved level {args.level} ({grid_size}x{grid_size}) "
          f"to content/{{en,uk}}/{args.category}/level-{args.level}.md")


if __name__ == "__main__":
    main()
