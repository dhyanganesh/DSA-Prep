# P3 · Outbreak Network

**Marks:** 40

## Story
A town's contact network has `N` people, numbered `1 … N`, and `M` friendships. Each
friendship is a mutual (undirected) link between two people. On **day 0**, a set of `K`
people are already infected. On each following day, the infection spreads from every
infected person to **all of their direct friends** at once; once infected, a person stays
infected.

Determine the day on which the **last person** becomes infected — that is, the number of
days until everyone in the town is infected. If some person can **never** be infected
(they have no chain of friendships to any initially-infected person), output `-1`.

## Input
- Line 1: three integers `N`, `M`, and `K`.
- Line 2: `K` integers — the ids of the initially infected people.
- Next `M` lines: two integers `u v` each, a friendship between `u` and `v`.

## Output
- A single integer: the day the last person is infected (the maximum over everyone of the
  days until they catch it), or `-1` if anyone can never be infected. If everyone is
  already infected on day 0, output `0`.

## Constraints
- `1 ≤ N ≤ 2·10^5`
- `0 ≤ M ≤ 4·10^5`
- `1 ≤ K ≤ N`
- friendships may repeat and are undirected; `1 ≤ u, v ≤ N`.

## Sample 1
```
Input
5 4 1
1
1 2
2 3
3 4
4 5

Output
4
```
Reason: the network is a chain `1—2—3—4—5` with only person `1` infected at day 0. Person
`5` is 4 links away, so is infected on day 4 — the last to fall.

## Sample 2
```
Input
4 2 1
1
1 2
3 4

Output
-1
```
Reason: people `3` and `4` form a separate component with no infected member, so they are
never infected.
