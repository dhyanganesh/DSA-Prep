# P1 · Toll Booth

**Marks:** 30

## Story
A highway toll booth logs the weights of `N` vehicles that passed through. The transport
authority then runs `Q` inspection queries; each query gives a weight limit `L`, and they
want to know **how many of the `N` vehicles weigh at most `L`**.

Answer all `Q` queries.

## Input
- Line 1: two integers `N` and `Q`.
- Line 2: `N` integers `w[0] … w[N-1]` — the vehicle weights (in arbitrary order).
- Line 3: `Q` integers `L[0] … L[Q-1]` — the query limits.

## Output
- `Q` lines: the `k`-th line is the number of vehicles with weight `≤ L[k]`.

## Constraints
- `1 ≤ N, Q ≤ 2·10^5`
- `1 ≤ w[i], L[k] ≤ 10^9`

## Sample 1
```
Input
5 2
3 1 4 1 5
3 5

Output
3
5
```
Explanation: weights sorted are `1 1 3 4 5`. Three are `≤ 3`; all five are `≤ 5`.

## Sample 2
```
Input
3 1
10 20 30
5

Output
0
```
Explanation: no vehicle weighs `≤ 5`.
