from solution import Solution, register
from typing import Iterable
from functools import reduce

@register("6_1")
class Day6(Solution):
    def solve(self):
        print(self.input)
        for line in self.input:
            print(line.replace('  ', ' ').split(' '))
        matrix = [
            [ int(x.strip()) for x in line.strip().split(' ') if x != '' ]
            for line in self.input[:-1]
        ]
        symbols = [ sym.strip() for sym in self.input[-1].split(' ') if sym != '' ]
        transpose = list(zip(*matrix))
        def prod(lst: Iterable):
            return reduce(int.__mul__, lst, 1)
        
        op = {
            '*': prod,
            '+': sum
        }
        for sym, col in zip(symbols, transpose):
            print(sym, col)
            result = op[sym](col)
            print(result)
        
        return sum((op[sym](col) for sym, col in zip(symbols, transpose)))

@register("6_2")
class Day6Part2(Solution):
    def solve(self):
        print(self.input)
        symbols = [ sym for sym in self.input[-1] if sym != ' ' ]

        indices = [ i for i, sym in enumerate(self.input[-1]) if sym != ' ' ] + [ len(self.input[0])+1 ]
        print(indices)
        matrix = [
            [ line[l:indices[i+1]-1] for i, l in enumerate(indices[:-1]) ]
            for line in self.input[:-1]
        ]

        for line in matrix:
            print(line)

        print(symbols)

        transpose = [
            [ int(s.strip()) for s in map(''.join, zip(*line)) ] # transpose again, join strings, and convert to int
            for line in list(zip(*matrix))
        ]

        for line in transpose:
            print(line)

        def prod(lst: Iterable):
            return reduce(int.__mul__, lst, 1)

        op = {
            '*': prod,
            '+': sum
        }
        for sym, col in zip(symbols, transpose):
            print(sym, col)
            result = op[sym](col)
            print(result)
        
        return sum((op[sym](col) for sym, col in zip(symbols, transpose)))
