import numpy as np
from solution import Solution, register
import matplotlib.pyplot as plt

@register("7_1")
class Day7(Solution):

    def generate_start(self, layout):
        beam = np.array([0 if sym == '.' else 1 for sym in layout])
        return beam
    
    def get_next_step(self, layout, current_step):
        splits = 0
        is_splitters = [0 if sym == '.' else 1 for sym in layout]

        next_step = np.copy(current_step)
        for i in range(len(layout)):
            if is_splitters[i] and current_step[i]: # if there there is a beam and it hits the splitter
                next_step[i] = 0
            
                # split the beam if there are no blockers (spliters are next to it)
                if 0 < i and not is_splitters[i - 1]:
                    next_step[i - 1] = 1
                if i < len(layout) -1 and not is_splitters[i + 1]:
                    next_step[i + 1] = 1

                    splits += 1

        return np.array(next_step), splits
    
    def generate_beam(self):
        lines = self.input
        beam = self.generate_start(lines[0])

        total_beam = [beam]
        total_splits = 0

        for line in lines[1:]:
            next_beam, splits = self.get_next_step(line, beam)

            total_beam.append(next_beam)
            total_splits += splits

            beam = next_beam
            
        return np.array(total_beam), total_splits

    def solve(self):
        print(self.input)

        beam, total_splits = self.generate_beam()
        return total_splits
        