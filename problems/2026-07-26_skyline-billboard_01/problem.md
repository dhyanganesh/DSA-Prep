# P3 · Skyline Billboard

**Marks:** 40

## Story
A city skyline is made of `N` adjacent buildings, each exactly 1 unit wide. Building `i`
has height `h[i]`. An advertiser wants to mount the **largest possible rectangular
billboard** flat against the skyline — the rectangle must be axis-aligned, rest on the
ground, and fit entirely within the buildings' silhouette (so a rectangle spanning a range
of buildings can only be as tall as the **shortest** building in that range).

Output the **maximum area** of such a rectangle.

## Input
- Line 1: an integer `N`.
- Line 2: `N` integers `h[0] … h[N-1]` — the building heights, left to right.

## Output
- A single integer: the largest rectangular area that fits under the skyline.

## Constraints
- `1 ≤ N ≤ 2·10^5`
- `0 ≤ h[i] ≤ 10^9`
- The area can be as large as about `2·10^14`.

## Sample 1
```
Input
6
2 1 5 6 2 3

Output
10
```
Explanation: buildings 3 and 4 (heights `5` and `6`) give a rectangle of height `5` over
width `2` → area `10`, the largest possible.

## Sample 2
```
Input
3
2 1 2

Output
3
```
Explanation: the best rectangle spans all three buildings at height `1` (area `3`), which
beats either single height-`2` building (area `2`).
