# Twin Couriers

**Difficulty:** Medium   **Time budget:** 45 minutes

## Story
A warehouse floor is an `R × C` grid of cells; entering cell `(i, j)` costs `w[i][j]`
energy. Two couriers set out at the same time:

- **Courier A** starts at the **top-left** `(0, 0)` and must reach the **bottom-right**
  `(R-1, C-1)`. On each step A moves **right** or **down** only.
- **Courier B** starts at the **top-right** `(0, C-1)` and must reach the **bottom-left**
  `(R-1, 0)`. On each step B moves **left** or **down** only.

Each courier travels the route that **minimises the total energy** it spends. The energy
of a route is the sum of `w` over every cell it visits, **including both its start and end
cells**. Let `d_A` be Courier A's minimum energy and `d_B` be Courier B's minimum energy.

Take `M = max(d_A, d_B)`.

Output **`1` if `M` is a prime number, otherwise `-1`.**

## Input
- Line 1: two integers `R` and `C`.
- Next `R` lines: each with `C` integers — row `i` gives `w[i][0] … w[i][C-1]`.

## Output
- A single integer: `1` if `M = max(d_A, d_B)` is prime, else `-1`.

## Constraints
- `1 ≤ R, C ≤ 500`
- `1 ≤ w[i][j] ≤ 1000`

## Sample 1
```
Input
3 3
1 3 1
1 5 1
4 2 1

Output
-1
```
Reason: Courier A's cheapest route `(0,0)→(0,1)→(0,2)→(1,2)→(2,2)` costs
`1+3+1+1+1 = 7`, so `d_A = 7`. Courier B's cheapest route
`(0,2)→(1,2)→(2,2)→(2,1)→(2,0)` costs `1+1+1+2+4 = 9`, so `d_B = 9`.
`M = max(7, 9) = 9`, which is not prime → `-1`.

## Sample 2
```
Input
2 2
1 1
1 1

Output
1
```
Reason: every route visits 3 cells of weight 1, so `d_A = d_B = 3`. `M = 3`, which is
prime → `1`.
