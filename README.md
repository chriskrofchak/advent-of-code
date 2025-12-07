# Advent of Code 2025 – Boilerplate

This repo is a small framework for solving Advent of Code 2025 problems with a shared structure and a simple registry / factory pattern for solutions.

## Layout

```text
.
├── main.py          # CLI / driver
├── solution.py      # base Solution class, registry + helpers
├── solutions/       # all puzzle-specific solution classes live here
│   ├── __init__.py
│   └── ...
├── examples/        # example inputs:  "<day>_<part>.txt", e.g. "1_1.txt"
├── inputs/          # real puzzle inputs: "<day>_<part>.txt"
└── outputs/         # where run() will write "<day>_<part>.txt"
```

We use an ID format of `"<day>_<part>"`, e.g.:
* `1_1` (day 1, part 1)
* `1_2` (day 1, part 2)
* `2_1`, `2_2`,

This same `"<day>_<part>"` string is used for:
* The registry key (e.g. `@register("1_1")`)
* The input / example / output filenames:
  * `examples/1_1.txt`
  * `inputs/1_1.txt`
  * `outputs/1_1.txt`

## How solutions work

All solutions subclass a common `Solution` base class in `solution.py` and register themselves with a decorator.

Base class

Each solution:
* Inherits from `Solution`
* Implements a `solve(self) -> str | int` method
* Gets raw input text via `self.raw_input`