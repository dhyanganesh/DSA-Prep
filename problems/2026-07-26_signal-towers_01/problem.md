# P3 · Signal Towers

**Marks:** 40

## Story
A telecom lays out `N` candidate mounting points along a straight highway, the `i`-th at
position `x[i]` (positions are distinct). They must switch on exactly `K` of these points
as signal towers. To minimise interference, they want the towers spread out: specifically,
they want to **maximise the minimum distance** between any two switched-on towers.

Choose which `K` positions to use so that the smallest gap between any two chosen towers is
as large as possible, and output that largest achievable minimum gap.

## Input
- Line 1: two integers `N` and `K`.
- Line 2: `N` space-separated integers `x[0] … x[N-1]` (all distinct).

## Output
- A single integer: the maximum possible value of the minimum distance between any two of
  the `K` chosen towers.

## Constraints
- `2 ≤ K ≤ N ≤ 2·10^5`
- `1 ≤ x[i] ≤ 10^9`, all `x[i]` distinct.

## Sample 1
```
Input
5 3
1 2 8 4 9

Output
3
```
Explanation: choosing positions `1, 4, 8` gives gaps `3` and `4`; the minimum gap is `3`,
and no choice of 3 towers does better.

## Sample 2
```
Input
4 2
10 1 5 7

Output
9
```
Explanation: with only 2 towers, place them at the extremes `1` and `10` for a gap of `9`.
