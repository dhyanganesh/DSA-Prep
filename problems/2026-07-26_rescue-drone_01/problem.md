# Rescue Drone

**Difficulty:** Medium   **Time budget:** 45 minutes

## Story
After an earthquake, a rescue drone must fly from the **top-left** corner `(0,0)` of a
building's floor plan to the **bottom-right** corner `(R-1, C-1)`. The floor plan is an
`R × C` grid where each cell is:

- `.` — open air the drone can fly through freely
- `#` — a cell blocked by rubble

The drone moves one cell at a time in the four cardinal directions (up, down, left,
right); each move takes **1 unit of time**. It carries `K` blast charges: to enter a
rubble cell it must spend **one** charge to clear it (entering an open cell costs nothing
extra). It may use at most `K` charges over the whole trip.

Find the **minimum time** to reach the bottom-right corner. If it cannot be reached even
using up to `K` charges, output `-1`.

The top-left and bottom-right cells are always open (`.`).

## Input
- Line 1: three integers `R`, `C`, and `K`.
- Next `R` lines: each a string of exactly `C` characters (`.` or `#`), top to bottom.

## Output
- A single integer: the minimum time to reach `(R-1, C-1)`, or `-1` if impossible.

## Constraints
- `1 ≤ R, C ≤ 100`
- `0 ≤ K ≤ 100`

## Sample 1
```
Input
3 5 1
..#..
..#..
..#..

Output
6
```
Reason: a full column of rubble separates the two sides. With 1 charge the drone clears
one rubble cell to cross, then reaches the corner in 6 moves (the shortest possible).

## Sample 2
```
Input
3 5 0
..#..
..#..
..#..

Output
-1
```
Reason: with no charges the rubble column cannot be crossed, so the corner is unreachable.
