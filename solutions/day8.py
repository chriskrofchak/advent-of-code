from solution import Solution, register
from itertools import combinations
from functools import reduce

def parse_input(inputs: list[str]):
    return [
        list(map(int, line.strip().split(',')))
        for line in inputs
    ]

def sort_points(points: list[list[int]]) -> list[tuple[int, int]]:
    # itertools will make tuple pairs of points
    # i keep track of indices to make life / printing easier
    def sq(x: int, y: int):
        return (x - y) ** 2

    def euclid(p: list[int], q: list[int]):
        return sum(map(lambda t: sq(*t), zip(p, q)))

    def distance(t: tuple[int, int]):
        i, j = t
        return euclid(points[i], points[j])

    return sorted(list(combinations(range(len(points)), 2)), key = distance)

def get_circuits(d: dict, i: int, j: int):
    # returns the number of the circuit including i or j
    # we will use this to determine if the boxes we are looking at
    # are in the same circuit, separate ones, or no circuit.
    return [
        k for k, v in d.items() if i in v or j in v
    ]

@register("8_1")
class Day7(Solution):
    def __init__(self, day_str, test = False):
        super().__init__(day_str, test)
        self.test = test

    def solve(self) -> int:
        stop = 10 if self.test else 1000
        circuits: dict[int, set[int]] = {}
        counter = 0
        for i, j in sort_points(parse_input(self.input))[:stop]:
            circuit_keys = get_circuits(circuits, i, j)
            match len(circuit_keys):
                case 0:
                    # don't exist - make a new circuit
                    circuits[counter] = { i, j }
                    counter += 1
                case 1:
                    # one box is in a circuit - add the other
                    circuits[ circuit_keys[0] ].update({ i, j }) # one is redundant, that's fine
                case 2:
                    # one box in one circuit, the other in the other,
                    # join circuits, pop one from the dictionary
                    keep, remove = circuit_keys
                    circuits[keep].update(circuits.pop(remove))

        sizes = [ len(v) for _, v in circuits.items() ]
        # return the product of the largest 3
        return reduce(int.__mul__, sorted(sizes, reverse=True)[:3])


@register("8_2")
class Day7Part2(Solution):
    def __init__(self, day_str, test = False):
         super().__init__(day_str, test)
         self.test = test

    def solve(self) -> int:
        stop = 10 if self.test else 1000
        circuits: dict[int, set[int]] = {}
        counter = 0
        points: list[list[int]] = parse_input(self.input)
        for i, j in sort_points(points):
            # print(i, j)
            circuit_keys = get_circuits(circuits, i, j)
            match len(circuit_keys):
                case 0:
                    # don't exist - make a new circuit
                    circuits[counter] = { i, j }
                    counter += 1
                    # print(counter)
                case 1:
                    # one box is in a circuit - add the other
                    circuits[ circuit_keys[0] ].update({ i, j }) # one is redundant, that's fine
                case 2:
                    # one box in one circuit, the other in the other,
                    # join circuits, pop one from the dictionary
                    keep, remove = circuit_keys
                    # print("Keeping", keep, "removing", remove)
                    circuits[keep].update(circuits.pop(remove))
            
            if len(circuits) == 1:
                _, v = list(circuits.items())[0]
                if v == set(range(len(points))):
                    print("Breaking now...")
                    break

        x1, _, _ = points[i]
        x2, _, _ = points[j]
        return x1 * x2
