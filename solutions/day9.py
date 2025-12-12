from solution import Solution, register
from dataclasses import dataclass
from itertools import combinations, product
from typing import Literal
from helpers import timeit

@dataclass
class Point:
    x: int
    y: int

    @property
    def tuple(self):
        return (self.x, self.y)

@dataclass
class Vector:
    dx: int
    dy: int
    n:  Literal["N", "E", "S", "W"]

### +x dirn ==>
### +y ||
###    \/

# note points are given in CLOCKWISE direction

###################
# CONSTANTS
###################

TL = (-1, -1)
TR = ( 1, -1)
BL = (-1,  1)
BR = ( 1,  1)

CORNER_MAP = {
    ('E', 'N'): TL,
    ('E', 'S'): TR,
    ('W', 'N'): BL,
    ('W', 'S'): BR,
    ('N', 'E'): TL,
    ('N', 'W'): BL,
    ('S', 'E'): TR,
    ('S', 'W'): BR,
}

CONVEX_MAP = {
    'S': 'W',
    'W': 'N',
    'N': 'E',
    'E': 'S'
}

###################
# HELPER FUNCTIONS
###################

def print_tiles(tiles: list[list[int]], points: list[Point]):
    for i, row in enumerate(tiles):
        for j, tile in enumerate(row):
            if any(((j, i) == point.tuple for point in points)):
                print("X", end = "")
            else:
                print("#" if tile else ".", end = "")
        print("") # end of row

def area(t: tuple[Point, Point]) -> int:
    p1, p2 = t
    x1, y1 = p1.tuple
    x2, y2 = p2.tuple
    return (max(x1,x2) - min(x1,x2) + 1) * (max(y1, y2) - min(y1, y2) + 1)

def compute_direction(dy: int, dx: int):
    assert dx == 0 or dy == 0 # only go in 1-D at a time
    dirn = ('E' if dx > 0 else 'W') if dx else ('S' if dy > 0 else 'N')
    return dirn

def point_diff(p: Point, next: Point) -> Vector:
    dy, dx = next.y - p.y, next.x - p.x
    return Vector(dx, dy, compute_direction(dy, dx))

def wedge(i: int, coords: list[Point]) -> tuple[Vector, Vector]:
    prev, curr, next_p = coords[i - 1], coords[i], coords[(i + 1) % len(coords)]
    vp, vn = point_diff(prev, curr), point_diff(curr, next_p)
    return vp, vn

def get_corner(i: int, coords: list[Point]) -> tuple[int, int]:
    vp, vn = wedge(i, coords)
    return CORNER_MAP[(vp.n, vn.n)]

def make_border(i: int, coords: list[Point]) -> tuple[Point, Point]:
    point: Point  = coords[i]
    j: int = (i + 1) % len(coords)
    next_p: Point = coords[j]
    c1x, c1y = get_corner(i, coords)
    c2x, c2y = get_corner(j, coords)
    return (
        Point(point.x + c1x, point.y + c1y),
        Point(next_p.x + c2x, next_p.y + c2y)
    )

@dataclass
class BorderRange:
    rx: int | range
    ry: int | range
    xy: Literal['x', 'y'] # x = horizontal, y = vertical

    def __post_init__(self):
        assert (
            isinstance(self.rx, int) and isinstance(self.ry, range) and self.xy == 'y'
            or isinstance(self.rx, range) and isinstance(self.ry, int) and self.xy == 'x'
        )

    def to_set(self):
        if self.xy == 'x':
            return list(product(list(self.rx), [self.ry]))
        else:
            assert self.xy == 'y'
            return list(product([self.rx], list(self.ry)))


def make_border_range(i: int, coords: list[Point]):
    p1: Point
    p2: Point
    p1, p2 = make_border(i, coords)
    v: Vector = point_diff(p1, p2)
    assert v.dy and p1.x == p2.x or v.dx and p1.y == p2.y
    return (
        BorderRange(p1.x, range(min(p1.y, p2.y), max(p1.y, p2.y) + 1), 'y')
        if v.dy else
        BorderRange(range(min(p1.x, p2.x), max(p1.x, p2.x) + 1), p1.y, 'x')
    )


def parse_input(lines: list[str]) -> list[Point]:
    return [ Point(*tuple(map(int, line.strip().split(',')))) for line in lines ]

@register("9_1")
class Day9(Solution):
    def solve(self) -> int:
        points: list[Point] = parse_input(self.input)
        return area(max(combinations(points, 2), key = area))

def east_ray(p: Point, ranges: list[BorderRange]):
    assert all((ray.xy == 'y' for ray in ranges))
    count = 0
    for ray in ranges:
        if ray.rx > p.x:
            break
        if p.y in ray.ry:
            count += 1
    return count

def south_ray(p: Point, ranges: list[BorderRange]):
    assert all((ray.xy == 'x' for ray in ranges))
    count = 0
    for ray in ranges:
        if ray.ry > p.y:
            break
        if p.x in ray.rx:
            count += 1
    return count

def assert_rectangle(p1: Point, p2: Point, verts: list[BorderRange], horiz: list[BorderRange]):
    x1, y1 = p1.tuple
    x2, y2 = p2.tuple

    # top left point, top right, bottom left, bottom right
    tl = Point(min(x1, x2), min(y1, y2))
    tr = Point(max(x1, x2), min(y1, y2))
    bl = Point(min(x1, x2), max(y1, y2))
    br = Point(max(x1, x2), max(y1, y2))

    # normally to check containment, we must check that count is odd
    # but we know two points are contained, so only equality is necessary
    # (namely, that any one edge does not escape the polygon)
    return (
            east_ray(tl, verts) == east_ray(tr, verts)
        and east_ray(bl, verts) == east_ray(br, verts)
        and south_ray(tl, horiz) == south_ray(bl, horiz)
        and south_ray(tr, horiz) == south_ray(br, horiz)
    )

@register("9_2")
class Day9Part2(Solution):
    def __init__(self, day_str, test = False):
        super().__init__(day_str, test)
        self.test = test

    @timeit
    def solve(self) -> int:
        points: list[Point] = parse_input(self.input)

        if self.test:
            tiles: list[list[int]] = [ [ 0 for _ in range(15) ] for _ in range(10) ]

            for p in points:
                tiles[p.y][p.x] = 1

        ranges: list[BorderRange] = []
        for i, p in enumerate(points):
            br: BorderRange = make_border_range(i, points)
            ranges.append(br)
            # print_tiles(tiles, list(map(lambda t: Point(*t), br.to_set())))
        
        verts = sorted(list(filter(lambda br: br.xy == 'y', ranges)), key = lambda br: br.rx)
        horiz = sorted(list(filter(lambda br: br.xy == 'x', ranges)), key = lambda br: br.ry)

        # for p1, p2 in combinations(points, 2):
        #     if assert_rectangle(p1, p2, verts, horiz):
        #         print_tiles(tiles, [p1, p2])
        #         print("With area:", area((p1, p2)))
        max_t = max(filter(lambda t: assert_rectangle(*t, verts, horiz), combinations(points, 2)), key = area)
        if self.test:
            print_tiles(tiles, [*max_t])
        print("With area:", area(max_t))
        return area(max_t)
