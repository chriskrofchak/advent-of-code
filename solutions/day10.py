from solution import Solution, register
import re
from dataclasses import dataclass
from copy import deepcopy
from functools import lru_cache

@dataclass
class SwitchContext:
    switches: list[int]
    toggles:  list[list[int]]
    joltages: list[int]

def mask(switches: list[int], toggle: set[int]):
    s2 = [ x for x in switches ]
    for i in toggle:
        s2[i] = 1 - s2[i] # toggle
    return s2

def parse_line(line: str) -> SwitchContext:

    switches: list[int] = list(map(lambda c: int(c == '#'), re.match(r'\[[\.#]+\]', line).group()[1:-1]))

    toggles: list[set[int]] = list(map(
        lambda s: set(map(int, s[1:-1].split(','))),
        map(lambda t: t[0], re.findall(r'(\(\d+(\,\d+)*\))', line))
    ))
    toggles: list[list[int]] = [
        mask([ 0 for _ in switches ], toggle) for toggle in toggles
    ]

    joltages = list(map(int, re.search(r'\{\d+(\,\d+)*\}', line).group()[1:-1].split(',')))

    return SwitchContext(switches=switches, toggles=toggles, joltages=joltages)

def parse_input(lines: str) -> list[SwitchContext]:
    return [ parse_line(line) for line in lines ]

def join(switch1: list[int], switch2: list[int]):
    return list(map(lambda t: sum(t)%2, zip(switch1, switch2)))

def join2(switch1: list[int], switch2: list[int]):
    return list(map(sum, zip(switch1, switch2)))

# top down...
def recur_helper(i: int, curr: list[int], toggles: list[set[int]], ctx: SwitchContext):
    if curr == ctx.switches:
        return i
    if len(toggles) == 0:
        return len(ctx.toggles)+100 # too big... bad answer.
    # else, min of including or excluding current one.
    return min(
        recur_helper(i+1, join(curr, toggles[0]), toggles[1:], ctx),
        recur_helper(i, curr, toggles[1:], ctx)
    )

def recur(ctx: SwitchContext):
    return recur_helper(0, [ 0 for _ in ctx.switches ], ctx.toggles, ctx)


def recur_joltage(ctx: SwitchContext):
    target = tuple(ctx.joltages)
    toggles = ctx.toggles
    n = max(target)
    INF = n*len(ctx.toggles) + 100 # bigger than solution

    @lru_cache(maxsize=None)
    def recur_helper_joltage(
            j: int,
            jolts: tuple[int, ...]) -> int:

        if jolts == target:
            return 0

        if j == len(toggles):
            return INF # nothing left.

        # else, min of including or excluding current one.
        toggle = toggles[j]

        best = INF
        for ii in range(n+1):
            if any((a > b for a,b in zip(jolts, target))):
                break # don't add anymore, too big

            best  = min(best, ii + recur_helper_joltage(j + 1, tuple(jolts)))
            jolts = join2(jolts, toggle)

        return best

    return recur_helper_joltage(0, tuple([ 0 for _ in ctx.switches ]))

@register("10_1")
class Day10(Solution):

    def solve(self) -> int:
        contexts: list[SwitchContext] = parse_input(self.input)
        total = 0
        for ctx in contexts:
            # print(ctx)
            total += recur(ctx)
        return total

@register("10_2")
class Day10Part2(Solution):

    def solve(self) -> int:
        contexts: list[SwitchContext] = parse_input(self.input)
        total = 0
        # for i, ctx in enumerate(contexts):
        #     x = recur_joltage(ctx)
        #     print(x)
        #     total += x

        print("Bounded by:", max(max(map(lambda ctx: ctx.joltages, contexts))))

        return total