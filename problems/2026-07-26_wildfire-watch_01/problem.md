# Wildfire Watch

**Difficulty:** Medium   **Time budget:** 45 minutes

## Story
A forest is laid out as a grid of `R` rows and `C` columns. Each cell is one of:

- `T` — a tree that has not yet caught fire
- `F` — a cell that is **already on fire** at minute 0 (there may be several, or none)
- `#` — bare rock: it never burns and fire cannot pass through it

Every minute, fire spreads from each burning cell to the trees in its four
directly-adjacent cells (up, down, left, right) — all burning cells spread at the same
time. Rock blocks the spread; fire cannot move diagonally or off the grid.

Determine the minute at which the **last tree** catches fire.

- If some tree can **never** catch fire, output `-1`.
- If there are **no trees** in the forest at all, output `0`.

## Input
- Line 1: two integers `R` and `C`.
- Next `R` lines: each a string of exactly `C` characters (`T`, `F`, or `#`) describing a
  row of the grid, top to bottom.

## Output
- A single integer: the minute the last tree catches fire (or `-1`, or `0`, as above).

## Constraints
- `1 ≤ R, C ≤ 1000`
- Each grid character is one of `T`, `F`, `#`.

## Sample 1
```
Input
3 4
FTTT
TT#T
TTTF

Output
2
```
Reason: fires start in the top-left and bottom-right corners and spread outward each
minute. The last trees to ignite (such as the top-right tree and the bottom-left tree)
catch fire 2 minutes in.

## Sample 2
```
Input
1 4
F#TT

Output
-1
```
Reason: the rock in column 2 blocks the fire, so the two trees to its right can never
catch fire.
