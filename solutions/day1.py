from helpers import expanded_reduce
from solution import Solution, register


def parse_rotation(rotation: str):
    dir = rotation[0]
    assert dir in {"L", "R"}
    x = int(rotation[1:])
    return -x if dir == "L" else x


@register("1_1")
class Day1(Solution):
    def __init__(self, day_str, test = False):
        super().__init__(day_str, test)
        self.ticker: int

    def solve(self):
        # print(self.input)
        positions = expanded_reduce(
            lambda l, r: (l + parse_rotation(r)) % 100,
            self.input,
            50
        )
        print(positions)
        return sum([ int(x == 0) for x in positions ])


@register("1_2")
class Day1Part2(Solution):
    def __init__(self, day_str, test = False):
        super().__init__(day_str, test)
        self.ticker: int

    def _rotate(self, l: int, r: int, inst: str):
        x = l

        t = int(inst[1:])
        d = inst[0]

        assert x in range(0, 100)
        assert d in {"L", "R"}
        for _ in range(t):
            if d == 'L':
                x -= 1
            else:
                x += 1
            x = x % 100
            if x == 0:
                self.ticker += 1

        return x

    def solve(self):
        print(self.input)
        self.ticker = 0
        positions = expanded_reduce(
            lambda l, r: self._rotate(l, parse_rotation(r), r),
            self.input,
            50
        )
        print(positions)
        return self.ticker