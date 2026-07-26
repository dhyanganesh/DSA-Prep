# Festival Stalls

**Difficulty:** Medium   **Time budget:** 45 minutes

## Story
A food festival has `N` stalls lined up in a row. Stall `i` serves a single cuisine,
identified by an integer type `c[i]` (two stalls with the same number serve the same
cuisine).

A visitor wants to stroll along a **contiguous** block of stalls and sample from each one,
but their stomach can only handle at most `K` **different** cuisines across the whole
block. They may eat any number of times from the same cuisine.

Find the **maximum number of stalls** in a contiguous block that contains at most `K`
distinct cuisine types.

## Input
- Line 1: two integers `N` and `K`.
- Line 2: `N` space-separated integers `c[1] … c[N]` — the cuisine type of each stall,
  left to right.

## Output
- A single integer: the length of the longest contiguous block of stalls using at most `K`
  distinct cuisines.

## Constraints
- `1 ≤ K ≤ N ≤ 2·10^5`
- `1 ≤ c[i] ≤ 10^9`

## Sample 1
```
Input
7 2
1 2 1 3 3 2 2

Output
4
```
Reason: the last four stalls (cuisines `3 3 2 2`) use only 2 distinct cuisines and form a
block of length 4; no longer contiguous block stays within 2 cuisines.

## Sample 2
```
Input
5 1
4 4 4 2 2

Output
3
```
Reason: with only 1 cuisine allowed, the three consecutive stalls serving cuisine `4` give
the longest valid block, length 3.
