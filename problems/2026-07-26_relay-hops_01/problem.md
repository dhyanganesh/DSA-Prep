# Relay Hops

**Difficulty:** Medium   **Time budget:** 45 minutes

## Story
A communications network has `N` relay stations, numbered `1 … N`, joined by `M`
bidirectional links. A signal starts at station `1` and must reach station `N`. Travelling
along one link counts as a single **hop**, and every link takes the same time regardless of
which two stations it connects.

Find the **minimum number of hops** to get a signal from station `1` to station `N`. If
station `N` cannot be reached from station `1`, output `-1`.

## Input
- Line 1: two integers `N` and `M`.
- Next `M` lines: two integers `u v` — a bidirectional link between stations `u` and `v`.

## Output
- A single integer: the fewest hops from station `1` to station `N`, or `-1` if it is
  unreachable. (If `N = 1`, the answer is `0`.)

## Constraints
- `1 ≤ N ≤ 2·10^5`
- `0 ≤ M ≤ 4·10^5`
- `1 ≤ u, v ≤ N`

## Sample 1
```
Input
4 3
1 2
2 3
3 4

Output
3
```
Reason: the only route is `1 → 2 → 3 → 4`, which is 3 hops.

## Sample 2
```
Input
4 2
1 2
3 4

Output
-1
```
Reason: stations `1,2` and `3,4` form separate groups; station `4` cannot be reached from
station `1`.
