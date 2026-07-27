# Island Survey

**Difficulty:** Medium   **Time budget:** 45 minutes

## Story
A satellite scan of an ocean region is delivered as an `R × C` grid. Each cell is either
land (`1`) or water (`0`). Two land cells belong to the same **island** if they are
adjacent horizontally or vertically (not diagonally), and an island is a maximal group of
land cells connected this way.

Report the **area of the largest island** — the number of land cells in the biggest
connected group. If there is no land at all, the answer is `0`.

## Input
- Line 1: two integers `R` and `C`.
- Next `R` lines: each a string of exactly `C` characters, each `0` (water) or `1` (land).

## Output
- A single integer: the number of cells in the largest island (`0` if there is none).

## Constraints
- `1 ≤ R, C ≤ 1000`
- every grid character is `0` or `1`

## Sample 1
```
Input
3 4
1101
1101
0001

Output
4
```
Reason: the top-left block of four `1`s is one island (area 4); the three `1`s down the
right edge form another island (area 3). The largest is 4.

## Sample 2
```
Input
2 2
00
00

Output
0
```
Reason: there is no land, so the largest island has area `0`.
