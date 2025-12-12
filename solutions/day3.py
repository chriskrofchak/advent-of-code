from solution import Solution, register
from helpers import find
from functools import partial

def battery(line: str):
    input = list(map(int, line))
    l = max(input[:-1])
    return 10*l + max(input[find(input, l)+1:])

@register("3_1")
class Day3(Solution):
    def solve(self):
        print(self.input)
        for line in self.input:
            line_battery = battery(line)
            print(line, line_battery)
        return sum(map(battery, self.input))

def battery_n(line: list[int], n: int):
    assert n >= 1, "What happened here."
    if n == 1:
        return [max(line)]
    l = max(line[:-(n - 1)])
    return [l] + battery_n(line[find(line, l)+1:], n - 1)


# an xn + an-1 xn-1 + ... a1x1 + a0
# a0 + x1(a1 + x2(a2 + .... + xn(an)))
def digit_to_int(digits: list[int]):
    def digit_helper(d: list[int]):
        return d[0] if len(d) == 1 else d[0] + 10*(digit_helper(d[1:]))
    return digit_helper(list(reversed(digits)))

def battery_str_n(n: int, line: str):
    assert n >= 1, "What happened here."
    if n == 1:
        return max(line)
    l = max(line[:-(n - 1)])
    return f'{l}{battery_str_n(n - 1, line[line.find(l)+1:])}'

@register("3_2")
class Day3Part3(Solution):
    def solve(self):
        print(self.input)
        for line in self.input:
            line_battery = battery_str_n(12, line)
            print(line, line_battery)
        return sum(map(int, map(partial(battery_str_n, 12), self.input)))