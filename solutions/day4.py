from solution import Solution, register

def _check_idx( A: list[list[int]], i: int, j: int):
    return i >= 0 and i < len(A) and j >= 0 and j < len(A[0])

def _get_neighbours( A: list[list[str]], i: int, j: int):
    nine = {-1, 0, 1}
    inds = [
        (n, m) for n in nine for m in nine if _check_idx(A, i+n, j+m) and (n,m) != (0,0)
    ]
    return [ A[i+n][j+m] for n, m in inds ]

def _check(A: list[list[str]], i: int, j: int):
    return A[i][j] == '@' and sum([ int(x == '@') for x in _get_neighbours(A, i, j) ]) < 4

def remove(inputs: list[str]) -> tuple[int, list[str]]:
    new_matrix = [
        [ 'x' if _check(inputs, i, j) else char for j, char in enumerate(line) ]
        for i, line in enumerate(inputs)
    ]
    for line in new_matrix:
        print(''.join(line))
    return sum(map(lambda line: sum([ int(x == 'x') for x in line]), new_matrix)), new_matrix

@register("4_1")
class Day4(Solution):
    def solve(self):
        removed, _ = remove(self.input)
        return removed


@register("4_2")
class Day4Part2(Solution):
    
    def solve(self):
        matrix = self.input
        total = 0
        i = 0
        while True:
            print(i+1, "===")
            removed, matrix = remove(matrix)
            delta = removed - total
            print("Removed:", delta)
            total += delta
            i += 1
            if delta == 0:
                break

        print("Removed", total, "rolls in", i, "iterations.")
        return total
