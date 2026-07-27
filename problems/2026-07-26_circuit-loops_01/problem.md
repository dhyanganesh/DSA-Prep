# Circuit Loops

**Difficulty:** Medium   **Time budget:** 45 minutes

## Story
A circuit board has `N` junctions, numbered `1 … N`, connected by `M` wires. Each wire
joins two distinct junctions, no two junctions are joined by more than one wire, and wires
have no direction. A **loop** is a closed path that starts and ends at the same junction
without reusing any wire.

Determine whether the wiring contains **at least one loop**. Output `1` if a loop exists,
`0` if the wiring is loop-free.

## Input
- Line 1: two integers `N` and `M`.
- Next `M` lines: two integers `u v` — a wire between junctions `u` and `v`
  (`u ≠ v`, and no wire is listed twice).

## Output
- A single integer: `1` if the circuit contains a loop, otherwise `0`.

## Constraints
- `1 ≤ N ≤ 2·10^5`
- `0 ≤ M ≤ 4·10^5`
- `1 ≤ u, v ≤ N`

## Sample 1
```
Input
3 3
1 2
2 3
3 1

Output
1
```
Reason: the wires `1–2`, `2–3`, `3–1` close a loop back to junction 1.

## Sample 2
```
Input
3 2
1 2
2 3

Output
0
```
Reason: the wiring is an open chain `1–2–3` with no way back to the start, so there is no
loop.
