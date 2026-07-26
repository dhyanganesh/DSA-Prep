# P2 · Playlist Run

**Marks:** 30

## Story
A road-trip playlist has `N` songs in a fixed order; song `i` lasts `d[i]` minutes. You
want to play a **contiguous run** of songs (consecutive in the list) whose total length
fits inside a time window of `S` minutes.

Find the **maximum number of songs** in a contiguous run whose durations sum to at most
`S`.

## Input
- Line 1: two integers `N` and `S`.
- Line 2: `N` integers `d[0] … d[N-1]` — the song durations, in playlist order.

## Output
- A single integer: the length of the longest contiguous run with total duration `≤ S`
  (`0` if even the shortest single song exceeds `S`).

## Constraints
- `1 ≤ N ≤ 2·10^5`
- `1 ≤ d[i] ≤ 10^9`
- `1 ≤ S ≤ 10^14`

## Sample 1
```
Input
5 4
1 2 1 1 3

Output
3
```
Explanation: the run `1 2 1` (songs 1–3) sums to `4 ≤ 4` and has length 3; no longer
contiguous run stays within 4.

## Sample 2
```
Input
3 4
5 6 7

Output
0
```
Explanation: every song alone already exceeds 4 minutes, so no run fits.
