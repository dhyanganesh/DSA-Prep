# Undercity Relay

**Difficulty:** Medium   **Time budget:** 45 minutes

## Story
A courier must carry a relay pack through the flooded undercity, modelled as an `R × C`
grid of tunnel cells. Each cell is either:

- **collapsed** — marked `-1`; it is blocked and cannot be entered, and
- **passable** — a positive integer giving the **effort** it costs to wade into that cell.

The courier starts at the top-left cell `(0, 0)` and must reach the bottom-right cell
`(R-1, C-1)`. From a cell they may step to any of the **four** orthogonally adjacent cells
(up, down, left, right) — there is no restriction to moving only toward the exit; the
tunnels wind, so the cheapest route may double back.

The **total effort** of a route is the sum of the effort values of every cell it enters,
**including both the start and the end cell**. Find the minimum possible total effort to
reach `(R-1, C-1)`. If the exit cannot be reached, output `-1`.

Both `(0, 0)` and `(R-1, C-1)` are always passable.

## Input
- Line 1: two integers `R` and `C`.
- Next `R` lines: each with `C` integers — row `i` gives the cells `(i, 0) … (i, C-1)`.
  A value of `-1` marks a collapsed (blocked) cell; any other value is a positive effort
  cost.

## Output
- A single integer: the minimum total effort from `(0, 0)` to `(R-1, C-1)`, or `-1` if it
  is unreachable.

## Constraints
- `1 ≤ R, C ≤ 200`
- Each cell is `-1` or an integer in `1 … 1000`.

## Sample 1
```
Input
3 3
1 2 2
1 9 2
1 1 1

Output
5
```
Reason: the cheapest route runs **down the left column then across the bottom row**:
`(0,0)→(1,0)→(2,0)→(2,1)→(2,2)`, effort `1+1+1+1+1 = 5`. Cutting through the middle `9` or
the right-hand `2`s costs more.

## Sample 2
```
Input
2 3
1 -1 1
1 -1 1

Output
-1
```
Reason: the entire middle column is collapsed, so the start (left column) is sealed off
from the exit (right column) — unreachable.
