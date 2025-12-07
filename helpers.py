from typing import Callable, Iterable




def find(lst: Iterable, item):
    """
    Returns the first index of item in lst,
    if it exists.

    Otherwise returns -1
    """
    for i, x in enumerate(lst):
        if item == x:
            return i

    return -1

def expanded_reduce(f: Callable, lst: Iterable, i) -> list:
    """
    Inputs:
    * f: a function that takes two arguments
    * lst: an iterable to iterate over
    * i: an initial value.

    Let lst = [a1,...,an]
    Let x1  = f(i, a1)
        x2  = f(x1, a2)
        ...
        xn  = f(xn-1, an)

    Returns [x1,...,xn]
    """
    return [
        (i := f(i, x)) for x in lst
    ]