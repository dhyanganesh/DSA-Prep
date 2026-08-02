"""
Disjoint Set Union (DSU / Union-Find) - standard reference template.

Python port of Striver's (takeuforward) C++ implementation, kept structurally
identical:
  - find() by recursion + path compression (the parent is reassigned on the way
    back up the recursion -> "backtracking" path compression)
  - Union by Rank
  - Union by Size

Nodes are 0..n: the constructor allocates n + 1 slots, so both 0-indexed and
1-indexed graphs work out of the box.

Complexity: every find / union is O(alpha(n)) amortised (inverse Ackermann,
effectively constant) once path compression and union by rank/size are combined.

Two find() variants are provided:
  - recursive + full path compression (active by default, matches Striver)
  - iterative path-halving (commented out, just below the recursive one) - no
    recursion, so it can't hit Python's stack limit on a deep chain. Swap it in
    when needed.
If you keep the recursive one and ever build long chains WITHOUT unioning, bump
the limit first:  import sys; sys.setrecursionlimit(1 << 20)
"""


class DisjointSet:
    def __init__(self, n):
        # slots 0..n so 1-indexed nodes (1..n) also work
        self.parent = list(range(n + 1))   # parent[i] = i  -> each node its own set
        self.rank = [0] * (n + 1)          # upper bound on tree height (union by rank)
        self.size = [1] * (n + 1)          # component size (union by size)

    def find(self, node):
        """Ultimate parent of `node`, with path compression on the backtrack."""
        if node == self.parent[node]:
            return node
        # recurse to the root, then compress: point `node` straight at the root
        self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    # --- iterative alternative: path halving (no recursion) ----------------
    # Same amortised cost as the recursive find with union by rank/size, but uses
    # O(1) stack, so it can't overflow on a deep chain. To switch, comment out the
    # recursive find() above and uncomment this one (same name, drop-in):
    #
    # def find(self, node):
    #     while node != self.parent[node]:
    #         self.parent[node] = self.parent[self.parent[node]]  # point at grandparent
    #         node = self.parent[node]
    #     return node

    def connected(self, u, v):
        """True if u and v are already in the same set."""
        return self.find(u) == self.find(v)

    def union_by_rank(self, u, v):
        pu, pv = self.find(u), self.find(v)
        if pu == pv:
            return                          # already together -> do nothing
        if self.rank[pu] < self.rank[pv]:
            self.parent[pu] = pv            # attach the shorter tree under the taller
        elif self.rank[pu] > self.rank[pv]:
            self.parent[pv] = pu
        else:
            self.parent[pv] = pu            # equal ranks: pick one root, bump its rank
            self.rank[pu] += 1

    def union_by_size(self, u, v):
        pu, pv = self.find(u), self.find(v)
        if pu == pv:
            return
        if self.size[pu] < self.size[pv]:
            self.parent[pu] = pv            # attach the smaller component under the larger
            self.size[pv] += self.size[pu]
        else:
            self.parent[pv] = pu
            self.size[pu] += self.size[pv]


if __name__ == "__main__":
    # Striver's walkthrough (7 nodes), using union by rank
    ds = DisjointSet(7)
    for a, b in [(1, 2), (2, 3), (4, 5), (6, 7), (5, 6)]:
        ds.union_by_rank(a, b)
    print("3 & 7 connected?", "Yes" if ds.connected(3, 7) else "No")   # No
    ds.union_by_rank(3, 7)
    print("3 & 7 connected?", "Yes" if ds.connected(3, 7) else "No")   # Yes

    # same edges, using union by size, then read a component's size
    ds2 = DisjointSet(7)
    for a, b in [(1, 2), (2, 3), (4, 5), (6, 7), (5, 6)]:
        ds2.union_by_size(a, b)
    print("size of 3's component:", ds2.size[ds2.find(3)])             # 3
    print("3 & 7 connected?", "Yes" if ds2.connected(3, 7) else "No")   # No
    ds2.union_by_size(3, 7)
    print("3 & 7 connected?", "Yes" if ds2.connected(3, 7) else "No") 
