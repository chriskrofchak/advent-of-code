import numpy as np
from solution import Solution, register

class UnionFind:
    def __init__(self, n):
        self.parent = np.arange(n)
        self.size = np.ones(n, dtype=int)
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

@register("8_2")
class Day8(Solution):
    def solve(self):
        coords = np.array([list(map(int, line.split(','))) for line in self.input])
        n = len(coords)
        xx, yy = np.meshgrid(np.arange(n), np.arange(n))
        diffs = coords[xx] - coords[yy]
        dists = np.linalg.norm(diffs, axis=2)
        i_upper, j_upper = np.triu_indices(n, k=1)
        edges = list(zip(dists[i_upper, j_upper], i_upper, j_upper))
        edges.sort(key=lambda t: t[0])


        uf1 = UnionFind(n)
        for _, i, j in edges[:10]: # change this number for n_closest pairs
            uf1.union(i, j)

        roots = [uf1.find(x) for x in range(n)]
        sizes = {}
        for r in roots:
            sizes[r] = sizes.get(r, 0) + 1

        part1_result = np.prod(sorted(sizes.values(), reverse=True)[:3])
        print("Part One:", part1_result)


        uf2 = UnionFind(n)
        last_edge = None
        for _, i, j in edges:
            merged = uf2.union(i, j)
            if merged:
                last_edge = (i, j)
            if uf2.components == 1:
                break

        i, j = last_edge
        part2_result = int(coords[i, 0]) * int(coords[j, 0])
        print("Part Two:", part2_result)

        return part1_result, part2_result