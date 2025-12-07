from argparse import ArgumentParser
from typing import Type
from solution import Solution, REGISTRY, BASE_DIR
import pkgutil
import importlib

def instantiate(pid: str, test: bool) -> Solution:
    cls: Type[Solution] = REGISTRY.get(pid)
    sol: Solution = cls(pid, test)
    return sol

def _auto_import_solutions():
    """
    Import all modules in the `solutions` package so that their
    @register decorators run and populate the registry.
    """
    import solutions  # this is the package

    package = solutions
    for module_info in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{package.__name__}.{module_info.name}")

def main() -> None:
    argparser = ArgumentParser()
    argparser.add_argument("puzzle_id",
                           help = (
                               "Pass the puzzle id: can pass just a day to do both, "
                               "or 1_1, 1_2, to do a particular one on a particular day."
                            ))
    argparser.add_argument("--test",  action="store_true", help="Test using the input in examples/")
    argparser.add_argument("--run",   action="store_true", help="Run using the input in inputs/")
    argparser.add_argument("--write", action="store_true", help="Write the run output to outputs/")

    args = argparser.parse_args()
    pid: str = args.puzzle_id

    pids = [pid] if '_' in pid else [f'{pid}_1', f'{pid}_2']
    print("Will run advent on", ', '.join(pids))

    _auto_import_solutions()

    if args.test:
        for _pid in pids:
            sol: Solution = instantiate(_pid, test = True)
            result = sol.solve()
            print("===== Test result for", _pid, "=====")
            print(result)

    if args.run:
        for _pid in pids:
            sol: Solution = instantiate(_pid, test = False)
            result = sol.solve()
            print("===== Run result for", _pid, "=====")
            print(result)
            if result is not None and args.write:
                (BASE_DIR / "outputs" / f'{_pid}.txt').write_text(str(result), encoding="utf-8")


if __name__ == "__main__":
    main()