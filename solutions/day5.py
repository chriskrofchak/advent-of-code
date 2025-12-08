from solution import Solution, register
from helpers import find
from functools import reduce
from dataclasses import dataclass
from random import randint

def parse_input(inputs: list[str]):
    i = find(inputs, "")
    ranges, ingredients = inputs[:i], inputs[i+1:]
    return (
        [ range(int(l), int(r) + 1) for l, r in map(lambda s: s.split('-'), ranges) ],
        list(map(int, ingredients))
    )

@register("5_1")
class Day5(Solution):
    def solve(self):
        ranges, ingredients = parse_input(self.input)
        print(ranges)
        print(ingredients)

        def in_ranges(ingredient: int):
            return any(map(lambda r: ingredient in r, ranges))

        return len(list(filter(in_ranges, ingredients)))

@dataclass
class BTree:
    x: range
    l: BTree | None = None
    r: BTree | None = None

def insert_btree(node: BTree | None, k: range) -> BTree:
    if node is None:
        return BTree(k)

    # else node exists
    if k.start < node.x.start:
        node.l = insert_btree(node.l, k)
    if k.start > node.x.start:
        node.r = insert_btree(node.r, k)
    if k.start == node.x.start:
        node.x = range(k.start, max(k.stop, node.x.stop))
    
    return node

def in_order(node: BTree | None):
    if node is None: return
    in_order(node.l)
    print(node.x)
    in_order(node.r)

def generate_inorder(node: BTree | None):
    if node is None:
        return
    yield from generate_inorder(node.l)
    yield node.x
    yield from generate_inorder(node.r)

@register("5_2")
class Day5Part2(Solution):
    def solve(self):
        ranges, _ = parse_input(self.input)

        # make BST
        assert len(ranges) > 1
        pivot = randint(0, len(ranges) - 1)
        root = BTree(ranges[pivot])
        for i, r in enumerate(ranges):
            if i == pivot:
                continue # already added
            root = insert_btree(root, r)

        # traverse BST
        prev = -1
        total = 0
        for ran in generate_inorder(root):
            ran: range
            l, r = ran.start, ran.stop
            print(ran, max(prev, l), r - max(prev, l))
            total += max(0, r - max(prev, l))
            prev = max(prev, r)
        return total
