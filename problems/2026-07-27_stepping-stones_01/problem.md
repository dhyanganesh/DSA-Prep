# P1 · Stepping Stones

**Marks:** 30

## Story
A river is crossed by `N` stones in a line, numbered `0 … N-1`. You start on stone `0` and
want to reach the far bank, which is stone `N-1`. Stone `i` is springy: from it you may leap
forward to any stone from `i+1` up to `i + a[i]` (a leap of length between 1 and `a[i]`). If
`a[i] = 0` the stone is dead and you cannot leap from it at all.

Find the **minimum number of leaps** needed to get from stone `0` to stone `N-1`. If it is
impossible to reach stone `N-1`, output `-1`.

## Input
- Line 1: an integer `N`.
- Line 2: `N` integers `a[0] … a[N-1]` — the maximum leap length from each stone.

## Output
- A single integer: the minimum number of leaps to reach stone `N-1`, or `-1` if it cannot
  be reached.

## Constraints
- `1 ≤ N ≤ 2·10^5`
- `0 ≤ a[i] ≤ N`

## Sample 1
```
Input
5
2 3 1 1 4

Output
2
```
Reason: leap `0 → 1` (length 1), then `1 → 4` (length 3). Two leaps reach the last stone,
and no single-leap route exists.

## Sample 2
```
Input
3
1 0 1

Output
-1
```
Reason: from stone `0` you can only reach stone `1`, which is dead (`a[1] = 0`), so stone
`2` is unreachable.
