# Watchtower Signals

**Difficulty:** Medium   **Time budget:** 45 minutes

## Story
Along the border stand `N` watchtowers in a straight west-to-east line. Tower `i` has
height `h[i]`. When a tower lights its beacon, the smoke drifts **eastward** (to the
right) and is noticed by exactly one tower: the **nearest tower to its east that is
strictly taller than it**. A tower of equal or lesser height cannot see over its own
parapet, so it does not notice the signal.

For every tower, the command post wants to know **how many towers away** that first
strictly-taller eastern tower is. If no tower to the east is strictly taller, the signal
is never noticed and the answer for that tower is `0`.

## Input
- Line 1: an integer `N`.
- Line 2: `N` space-separated integers `h[1] … h[N]` (heights, west to east).

## Output
- One line with `N` space-separated integers `d[1] … d[N]`, where `d[i]` is the distance
  (in tower positions) to the nearest strictly taller tower east of tower `i`, or `0` if
  there is none.

## Constraints
- `1 ≤ N ≤ 2·10^5`
- `1 ≤ h[i] ≤ 10^9`

## Sample 1
```
Input
5
3 1 4 1 5

Output
2 1 2 1 0
```
Reason: tower 1 (h=3) → tower 3 (h=4) is the nearest taller, 2 positions away. Tower 2
(h=1) → tower 3, 1 away. Tower 3 (h=4) → tower 5 (h=5), 2 away. Tower 4 (h=1) → tower 5,
1 away. Tower 5 has nothing taller to its east → 0.

## Sample 2
```
Input
4
4 3 3 5

Output
3 2 1 0
```
Reason: tower 1 (h=4) → tower 4 (h=5), 3 away. The two towers of height 3 are **not**
taller than each other, so tower 2 → tower 4 (2 away) and tower 3 → tower 4 (1 away).
Tower 4 is the tallest to the east → 0.
