from solution import Solution, register
from helpers import find

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