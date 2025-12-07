from abc import ABC, abstractmethod
from typing import Type
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Solution(ABC):
    """
    Simple Abstract Base Class for solving the Advent of Code
    """
    def __init__(self, day_str: str, test: bool = False):
        super().__init__()
        input_dir = "examples" if test else "inputs"
        with open(BASE_DIR / input_dir / f"{day_str}.txt", "r", encoding = "utf-8") as f:
            lines = f.read().splitlines()
        self.input: list[str] = lines

    @abstractmethod
    def solve(self):
        """
        Implement this in your inherited class to solve the advent problem.
        """

    def check(self):
        print("Showing input:")
        for line in self.input:
            print(line)

REGISTRY: dict[str, Type[Solution]] = {}

def register(puzzle_id: str):
    """
    Class decorator to register a Solution subclass for a given puzzle ID.

    Usage:

        @register("1_1")
        class Day1Part1(Solution):
            ...

    The puzzle_id MUST follow the "<day>_<part>" convention, e.g. "3_2".
    """
    if "_" not in puzzle_id:
        raise ValueError(f"puzzle_id must look like 'day_part', got {puzzle_id!r}")

    def decorator(cls: Type[Solution]) -> Type[Solution]:
        if puzzle_id in REGISTRY:
            prev = REGISTRY[puzzle_id].__name__
            raise ValueError(
                f"Puzzle ID '{puzzle_id}' is already registered "
                f"to {prev}; cannot register {cls.__name__}"
            )

        REGISTRY[puzzle_id] = cls
        # # optional: attach the id to the class
        # cls.puzzle_id = puzzle_id  # type: ignore[attr-defined]
        return cls

    return decorator