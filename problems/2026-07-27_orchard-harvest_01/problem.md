# P2 · Orchard Harvest

**Marks:** 30

## Story
An orchard has `N` fields; field `i` holds `a[i]` ripe crops. A single harvesting drone
works one field at a time. If the drone is set to a picking **rate** of `r` crops per hour,
then clearing a field of `s` crops takes `ceil(s / r)` hours (a partly-picked hour still
counts as a whole hour, and the drone never splits an hour across two fields).

A storm arrives in `H` hours, so every field must be fully cleared within `H` hours total.
Find the **minimum integer rate `r`** that lets the drone finish all `N` fields in time.

## Input
- Line 1: two integers `N` and `H`.
- Line 2: `N` integers `a[0] … a[N-1]` — the crops in each field.

## Output
- A single integer: the smallest rate `r` such that `sum(ceil(a[i] / r)) ≤ H`.

## Constraints
- `1 ≤ N ≤ 2·10^5`
- `1 ≤ a[i] ≤ 10^9`
- `N ≤ H ≤ 10^14`

## Sample 1
```
Input
4 8
3 6 7 11

Output
4
```
Reason: at rate `4` the fields take `1 + 2 + 2 + 3 = 8` hours (exactly `H`); at rate `3`
they need `1 + 2 + 3 + 4 = 10 > 8`.

## Sample 2
```
Input
5 5
30 11 23 4 20

Output
30
```
Reason: with only `5` hours for `5` fields, each field gets one hour, so the rate must
clear the largest field (`30`) in a single hour → `r = 30`.
