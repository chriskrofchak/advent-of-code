from solution import Solution, register

def make_newline(beamlist: list[int], beamline: str):
    return ''.join([ '|' if b == 1 and x != '^' else x for b, x in zip(beamlist, beamline) ])

def split_beams(prev: str, beamline: str):
    """
    Takes a beam line and the previous line and splits the beams
    """
    beamlist = [ 0 for _ in beamline ]
    splits = 0
    for i, (p, x) in enumerate(zip(prev, beamline)):
        # base case
        if p == 'S' or p == '|':
            beamlist[i] = 1

        if p == '|' and x == '^':
            splits += 1
            if i > 0:
                beamlist[i - 1] = 1

            if i < len(beamline) - 1:
                beamlist[i + 1] = 1

    return splits, make_newline(beamlist, beamline)

def split_beams_nd(prev: list[int], beamline: str):
    """
    Takes a beam line and the previous line and splits the beams
    """
    beamlist = [ 0 for _ in beamline ]
    for i, (p, x) in enumerate(zip(prev, beamline)):
        # base case
        if p > 0:
            beamlist[i] += p

        if x == '^':
            beamlist[i] = 0

            if i > 0:
                beamlist[i - 1] += p

            if i < len(beamline) - 1:
                beamlist[i + 1] += p

    return beamlist

@register("7_1")
class Day7(Solution):

    def solve(self) -> int:
        prev = self.input[0]
        total = 0
        outs = [self.input[0]]
        for line in self.input[1:]:
            splits, newline = split_beams(prev, line)
            total += splits
            prev = newline
            outs.append(newline)

        for line in outs:
            print(line)
        print(total)
        return total

@register("7_2")
class Day7Part2(Solution):

        def solve(self) -> int:
            prev = [ int(x == 'S') for x in self.input[0] ]

            for line in self.input[1:]:
                prev = split_beams_nd(prev, line)
    
            print(sum(prev))
            return sum(prev)
