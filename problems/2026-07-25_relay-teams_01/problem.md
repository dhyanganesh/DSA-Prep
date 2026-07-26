# Relay Squad

**Difficulty:** Medium   **Time budget:** 45 minutes

## Story
Coach Rao is forming relay teams for the SWPCT sports meet. There are `N` runners
standing in a fixed line, and the coach is **not allowed to reorder them** — a team must
be a block of consecutive runners from the line.

He must split the whole line into **exactly `K` non-empty teams**, each team being a
contiguous group. A team's *strength* is the sum of the speeds of the runners in it.
The squad's *fatigue* is the strength of its **strongest** team.

Coach Rao wants the fairest split: choose the `K` teams so that the **fatigue (the
maximum team strength) is as small as possible**. Report that minimum possible fatigue.

## Input
- Line 1: two integers `N` and `K`.
- Line 2: `N` space-separated integers — the speeds `a[1] … a[N]` in line order.

## Output
- A single integer: the minimum possible fatigue (smallest achievable maximum team
  strength when the line is split into exactly `K` contiguous teams).

## Constraints
- `1 ≤ K ≤ N ≤ 10^5`
- `1 ≤ a[i] ≤ 10^4`
- The total of all speeds can be up to `10^9`.

## Sample 1
```
Input
5 2
7 2 5 10 8

Output
18
```
Reason: teams `(7,2,5)` and `(10,8)` have strengths `14` and `18`; the max is `18`, and
no split into 2 contiguous teams does better.

## Sample 2
```
Input
4 3
1 4 4 3

Output
5
```
Reason: teams `(1,4)`, `(4)`, `(3)` have strengths `5, 4, 3`; the max is `5`, the smallest
possible for 3 contiguous teams.
