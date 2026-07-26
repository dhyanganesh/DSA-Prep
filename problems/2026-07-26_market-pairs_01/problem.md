# P1 · Market Pairs

**Marks:** 30

## Story
A street market has `N` stalls, and stall `i` charges a price `a[i]`. A shopper has a
budget `B` and wants to know how many **different pairs of stalls** they could visit
together while keeping the combined price within budget.

Count the number of **unordered pairs** `(i, j)` with `i < j` such that
`a[i] + a[j] ≤ B`.

## Input
- Line 1: two integers `N` and `B`.
- Line 2: `N` space-separated integers `a[0] … a[N-1]`.

## Output
- A single integer: the number of pairs whose prices sum to at most `B`.

## Constraints
- `1 ≤ N ≤ 2·10^5`
- `1 ≤ a[i] ≤ 10^9`
- `1 ≤ B ≤ 2·10^9`
- The answer can exceed 32 bits.

## Sample 1
```
Input
5 6
1 5 3 3 2

Output
7
```
Explanation: the qualifying pairs (by value) are `1+5, 1+3, 1+3, 1+2, 2+3, 2+3, 3+3` — 7
pairs with sum ≤ 6.

## Sample 2
```
Input
4 4
1 1 1 1

Output
6
```
Explanation: every one of the `C(4,2) = 6` pairs sums to `2 ≤ 4`.
