# Faction Split

**Difficulty:** Medium   **Time budget:** 45 minutes

## Story
A guild has `N` members, numbered `1 … N`. There are `M` known **rivalries**, each a mutual
grudge between two members. The guildmaster wants to divide **every** member into exactly
two factions so that no rivalry falls inside a single faction — i.e. the two members of
every rivalry end up in **different** factions.

Decide whether such a split is possible. Output `1` if it is, `0` if it is not.

## Input
- Line 1: two integers `N` and `M`.
- Next `M` lines: two integers `u v` — a rivalry between members `u` and `v`
  (`u ≠ v`, and no rivalry is listed twice).

## Output
- A single integer: `1` if the members can be split into two rivalry-free factions,
  otherwise `0`.

## Constraints
- `1 ≤ N ≤ 2·10^5`
- `0 ≤ M ≤ 4·10^5`
- `1 ≤ u, v ≤ N`

## Sample 1
```
Input
4 4
1 2
2 3
3 4
4 1

Output
1
```
Reason: put `{1, 3}` in one faction and `{2, 4}` in the other; every rivalry crosses the
two factions.

## Sample 2
```
Input
3 3
1 2
2 3
3 1

Output
0
```
Reason: the three members all rival each other (a triangle); any 2-way split forces some
rivalry into the same faction.
