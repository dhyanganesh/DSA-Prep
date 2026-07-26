# P2 · Stage Acts

**Marks:** 30

## Story
A festival has a single stage and `N` acts have applied to perform. Act `i` wants to run
from time `s[i]` to time `e[i]` (with `s[i] < e[i]`); while it performs it occupies the
stage over the half-open interval `[s[i], e[i])`. Two acts **conflict** if their
performance intervals overlap — but one act may start **exactly** when another finishes
(so `[1, 3)` and `[3, 5)` are fine together).

The organiser wants to schedule as many acts as possible on the one stage with no
conflicts. Output the **maximum number of acts** that can be scheduled.

## Input
- Line 1: an integer `N`.
- Next `N` lines: two integers `s[i]` and `e[i]` — the start and end of act `i`.

## Output
- A single integer: the largest number of pairwise non-conflicting acts.

## Constraints
- `1 ≤ N ≤ 2·10^5`
- `0 ≤ s[i] < e[i] ≤ 10^9`

## Sample 1
```
Input
3
1 3
2 5
4 7

Output
2
```
Explanation: `[1,3)` and `[4,7)` don't conflict, giving 2 acts. `[2,5)` overlaps both, so
you can't fit all three.

## Sample 2
```
Input
4
1 2
2 3
3 4
1 4

Output
3
```
Explanation: `[1,2)`, `[2,3)`, `[3,4)` chain back-to-back (touching is allowed) for 3 acts;
`[1,4)` conflicts with all of them.
