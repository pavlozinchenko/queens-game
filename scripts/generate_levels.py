#!/usr/bin/env python3
"""
Queens Game — level generator.

Usage:
  python generate_levels.py easy            # 1 easy level (4-5)
  python generate_levels.py medium          # 1 medium level (6-7)
  python generate_levels.py hard            # 1 hard level (8-9)
  python generate_levels.py --size 6        # 1 level of size 6x6

Outputs the grid to stdout. Save manually to content files.
"""

import argparse
import random
import sys
import string
import time
from collections import deque

DIFFICULTY_SIZES = {
    "easy": [4, 5],
    "medium": [6, 7],
    "hard": [8, 9],
}

DIFFICULTY_LABELS = {
    4: "Easy", 5: "Easy",
    6: "Medium", 7: "Medium",
    8: "Hard", 9: "Hard",
}


def find_placement(n):
    cols = []
    used = set()

    def solve():
        row = len(cols)
        if row == n:
            return True
        candidates = list(range(n))
        random.shuffle(candidates)
        for c in candidates:
            if c in used:
                continue
            if cols and abs(cols[-1] - c) <= 1:
                continue
            cols.append(c)
            used.add(c)
            if solve():
                return True
            cols.pop()
            used.discard(c)
        return False

    if solve():
        return [(r, cols[r]) for r in range(n)]
    return None


def build_voronoi(n, queens):
    grid = [[-1] * n for _ in range(n)]
    jitter = {i: random.random() * 0.8 for i in range(n)}
    for r in range(n):
        for c in range(n):
            best_dist = float("inf")
            best_idx = -1
            for idx, (qr, qc) in enumerate(queens):
                d = abs(r - qr) + abs(c - qc) + jitter[idx]
                if d < best_dist:
                    best_dist = d
                    best_idx = idx
            grid[r][c] = best_idx
    return grid


def build_bfs(n, queens):
    grid = [[-1] * n for _ in range(n)]
    frontiers = []
    for idx, (r, c) in enumerate(queens):
        grid[r][c] = idx
        frontiers.append(deque([(r, c)]))
    while any(frontiers):
        order = list(range(n))
        random.shuffle(order)
        for idx in order:
            if not frontiers[idx]:
                continue
            next_f = deque()
            while frontiers[idx]:
                r, c = frontiers[idx].popleft()
                dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                random.shuffle(dirs)
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == -1:
                        grid[nr][nc] = idx
                        next_f.append((nr, nc))
            frontiers[idx] = next_f
    return grid


def is_contiguous(grid, n, region_id):
    start = None
    total = 0
    for r in range(n):
        for c in range(n):
            if grid[r][c] == region_id:
                total += 1
                if start is None:
                    start = (r, c)
    if not start:
        return False
    visited = {start}
    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) not in visited and 0 <= nr < n and 0 <= nc < n \
               and grid[nr][nc] == region_id:
                visited.add((nr, nc))
                queue.append((nr, nc))
    return len(visited) == total


def find_solutions(n, grid, limit=10):
    regions = [[] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            regions[grid[r][c]].append((r, c))

    order = sorted(range(n), key=lambda i: len(regions[i]))
    sorted_regions = [regions[i] for i in order]

    solutions = []
    used_r = [False] * n
    used_c = [False] * n
    placed = []

    def solve(idx):
        if len(solutions) >= limit:
            return
        if idx == n:
            solutions.append(list(placed))
            return
        for r, c in sorted_regions[idx]:
            if used_r[r] or used_c[c]:
                continue
            adj = False
            for pr, pc in placed:
                if abs(pr - r) <= 1 and abs(pc - c) <= 1:
                    adj = True
                    break
            if adj:
                continue
            used_r[r] = True
            used_c[c] = True
            placed.append((r, c))
            solve(idx + 1)
            used_r[r] = False
            used_c[c] = False
            placed.pop()

    solve(0)
    return solutions


def fix_uniqueness(n, grid, queens, max_iters=300, progress_cb=None):
    queen_set = set(queens)

    for iteration in range(max_iters):
        solutions = find_solutions(n, grid, limit=5)

        if progress_cb:
            progress_cb(iteration, max_iters, len(solutions))

        if len(solutions) == 1:
            return True
        if len(solutions) == 0:
            return False

        # Find where solutions disagree and swap cells there
        target = solutions[0]
        alt = solutions[1]
        diff_cells = []
        for t, a in zip(target, alt):
            if t != a:
                diff_cells.extend([t, a])

        if not diff_cells:
            return False

        # Try swaps near disagreement
        improved = False
        random.shuffle(diff_cells)
        for base_r, base_c in diff_cells:
            if improved:
                break
            for dr in range(-1, 2):
                if improved:
                    break
                for dc in range(-1, 2):
                    r, c = base_r + dr, base_c + dc
                    if not (0 <= r < n and 0 <= c < n):
                        continue
                    if (r, c) in queen_set:
                        continue

                    old_reg = grid[r][c]
                    neighbors = set()
                    for ndr, ndc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + ndr, c + ndc
                        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] != old_reg:
                            neighbors.add(grid[nr][nc])

                    for new_reg in neighbors:
                        grid[r][c] = new_reg
                        if is_contiguous(grid, n, old_reg):
                            new_sols = find_solutions(n, grid, limit=5)
                            if len(new_sols) < len(solutions):
                                improved = True
                                break
                        grid[r][c] = old_reg

        if not improved:
            # Random fallback swap
            for _ in range(20):
                r, c = random.randint(0, n-1), random.randint(0, n-1)
                if (r, c) in queen_set:
                    continue
                old_reg = grid[r][c]
                neighbors = set()
                for ndr, ndc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + ndr, c + ndc
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] != old_reg:
                        neighbors.add(grid[nr][nc])
                if neighbors:
                    new_reg = random.choice(list(neighbors))
                    grid[r][c] = new_reg
                    if not is_contiguous(grid, n, old_reg):
                        grid[r][c] = old_reg
                    break

    solutions = find_solutions(n, grid, limit=2)
    return len(solutions) == 1


def generate_level(n, max_attempts=30):
    builders = [build_voronoi, build_bfs]
    start = time.time()

    for attempt in range(max_attempts):
        queens = find_placement(n)
        if queens is None:
            continue

        builder = random.choice(builders)
        grid = builder(n, queens)

        region_set = set()
        for r in range(n):
            for c in range(n):
                region_set.add(grid[r][c])
        if len(region_set) != n:
            continue

        elapsed = time.time() - start

        def progress(iteration, total, num_solutions):
            e = time.time() - start
            bar_len = 20
            pct = iteration / total
            filled = int(bar_len * pct)
            bar = "█" * filled + "░" * (bar_len - filled)
            print(f"\r  attempt {attempt+1}/{max_attempts} |{bar}| "
                  f"iter {iteration}/{total} sols={num_solutions} "
                  f"{e:.1f}s", end="", file=sys.stderr, flush=True)

        if fix_uniqueness(n, grid, queens, progress_cb=progress):
            print(f"\r" + " " * 80 + "\r", end="", file=sys.stderr)
            return grid

        print(f"\r" + " " * 80 + "\r", end="")

    return None


def grid_to_string(grid):
    n = len(grid)
    letters = string.ascii_lowercase
    return "\n".join(
        "".join(letters[grid[r][c]] for c in range(n)) for r in range(n)
    )



def main():
    parser = argparse.ArgumentParser(
        description="Queens Game level generator",
        usage="%(prog)s (easy|medium|hard | --size N)",
    )
    parser.add_argument("difficulty", nargs="?",
                        choices=["easy", "medium", "hard"],
                        help="Difficulty preset")
    parser.add_argument("--size", type=int,
                        help="Exact grid size (overrides difficulty)")
    args = parser.parse_args()

    if args.size:
        sizes = [args.size]
        difficulty = DIFFICULTY_LABELS.get(args.size, "Medium")
    elif args.difficulty:
        sizes = DIFFICULTY_SIZES[args.difficulty]
        difficulty = args.difficulty.capitalize()
    else:
        parser.error("Provide difficulty (easy/medium/hard) or --size N")

    n = random.choice(sizes)

    print(f"Generating {difficulty} ({n}x{n})...\n", file=sys.stderr, flush=True)

    t0 = time.time()
    grid = generate_level(n)
    elapsed = time.time() - t0

    if grid is None:
        print(f"\nFAILED ({elapsed:.1f}s)", file=sys.stderr)
        sys.exit(1)

    grid_str = grid_to_string(grid)
    print(f"\n✓ {n}x{n} {difficulty} — {elapsed:.1f}s", file=sys.stderr)

    # Output grid to stdout
    print(grid_str)


if __name__ == "__main__":
    main()
