from solution import Solution, register
import re

@register("2_1")
class Day2(Solution):
    def __init__(self, day_str, test = False):
        super().__init__(day_str, test)
        self.ticker: int

    def solve(self):
        inputs = self.input[0].split(',')
        return sum([
            sum(map(int,
                    filter(lambda x: x[:(t := len(x) // 2)] == x[t:],
                           filter(lambda x: len(x) % 2 == 0,
                                  map(str, range(int(l), int(r) + 1))))))
            for l, r in map(lambda s: s.split('-'), inputs)
        ])


@register("2_2")
class Day2Part2(Solution):
    def __init__(self, day_str, test = False):
        super().__init__(day_str, test)
        self.ticker: int

    def _repetitions(self, x: str):
        n = len(x) // 2
        for i in range(1, n+1):
            substr = x[:i]
            m = re.match(f'({substr})+', x)
            if m and m.group() == x:
                print(x)
                return True

        return False

    def solve(self):
        inputs = self.input[0].split(',')
        return sum([
            sum(map(int,
                    filter(self._repetitions,
                           map(str, range(int(l), int(r) + 1)))))
            for l, r in map(lambda s: s.split('-'), inputs)
        ])

