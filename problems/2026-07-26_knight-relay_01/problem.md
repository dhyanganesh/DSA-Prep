# Knight Relay

**Difficulty:** Medium   **Time budget:** 45 minutes

## Story
A messenger knight stands on an `N × N` board whose rows and columns are numbered
`1 … N`. The knight moves exactly like a chess knight: each move shifts it by `(±1, ±2)`
or `(±2, ±1)`, and it may never step off the board.

Starting at square `(r1, c1)`, the knight must deliver a message to square `(r2, c2)`.
Find the **minimum number of moves** to get there, or `-1` if it is impossible.

## Input
- Line 1: an integer `N`.
- Line 2: four integers `r1 c1 r2 c2` — the start row/column and the target row/column
  (all in `1 … N`).

## Output
- A single integer: the fewest knight moves from `(r1, c1)` to `(r2, c2)`, or `-1` if the
  target cannot be reached. (If start equals target, the answer is `0`.)

## Constraints
- `1 ≤ N ≤ 1000`
- `1 ≤ r1, c1, r2, c2 ≤ N`

## Sample 1
```
Input
8
1 1 2 3

Output
1
```
Reason: from `(1,1)` a single knight move `(+1, +2)` lands on `(2,3)`.

## Sample 2
```
Input
8
1 1 8 8

Output
6
```
Reason: the shortest knight route from one corner of a standard board to the opposite
corner takes 6 moves.
