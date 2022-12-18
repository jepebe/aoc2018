import typing

from aoc.tester import Tester


class Tuple3:
    __match_args__ = ("x", "y", "z")

    def __init__(self, x, y, z):
        self._v = (x, y, z)
        self._hash = self._v.__hash__()

    @property
    def x(self):
        return self._v[0]

    @property
    def y(self):
        return self._v[1]

    @property
    def z(self):
        return self._v[2]

    def __getitem__(self, item):
        return self._v[item]

    def __add__(self, other):
        match other:
            case (x, y, z) | Tuple3(x, y, z):
                return Tuple3(self.x + x, self.y + y, self.z + z)
            case _:
                self._operator_exception("+", other)

    def __sub__(self, other):
        match other:
            case (x, y, z) | Tuple3(x, y, z):
                return Tuple3(self.x - x, self.y - y, self.z - z)
            case _:
                self._operator_exception("-", other)

    def __lt__(self, other):
        match other:
            case (x, y, z) | Tuple3(x, y, z):
                return self.x < x and self.y < y and self.z < z
            case _:
                self._operator_exception("<", other)

    def __le__(self, other):
        match other:
            case (x, y, z) | Tuple3(x, y, z):
                return self.x <= x and self.y <= y and self.z <= z
            case _:
                self._operator_exception("<=", other)

    def __gt__(self, other):
        match other:
            case (x, y, z) | Tuple3(x, y, z):
                return self.x > x and self.y > y and self.z > z
            case _:
                self._operator_exception(">", other)

    def __ge__(self, other):
        match other:
            case (x, y, z) | Tuple3(x, y, z):
                return self.x >= x and self.y >= y and self.z >= z
            case _:
                self._operator_exception(">=", other)

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        if isinstance(other, Tuple3):
            other = other._v
        return self._v == other

    def __hash__(self):
        return self._hash

    def __repr__(self):
        return f"Tuple3({self.x}, {self.y}, {self.z})"

    def _operator_exception(self, op, other):
        self_type = type(self).__name__
        other_type = type(other).__name__
        raise TypeError(f" '{op}' not supported between instances of '{self_type}' and '{other_type}'")


def cube_extents(points: typing.Iterable[tuple[int, int, int] | Tuple3]) -> tuple[Tuple3, Tuple3]:
    min_x = min(c.x for c in points)
    max_x = max(c.x for c in points)
    min_y = min(c.y for c in points)
    max_y = max(c.y for c in points)
    min_z = min(c.z for c in points)
    max_z = max(c.z for c in points)
    return Tuple3(min_x, min_y, min_z), Tuple3(max_x, max_y, max_z)


if __name__ == '__main__':
    t = Tester("tuple3")

    v = Tuple3(1, 2, 3)
    u = Tuple3(11, 17, 23)

    t.test_section("subscript and fields")
    t.test_value(v.x, 1)
    t.test_value(v[0], 1)
    t.test_value(v.y, 2)
    t.test_value(v[1], 2)
    t.test_value(v.z, 3)
    t.test_value(v[2], 3)

    t.test_section("add")
    t.test_value(v + u, Tuple3(12, 19, 26))
    t.test_value(v + (1, 2, 3), Tuple3(2, 4, 6))

    try:
        _ = v + 5
        t.test(False)
    except TypeError:
        t.test(True)

    t.test_section("subtract")
    t.test_value(v - u, Tuple3(-10, -15, -20))
    t.test_value(v - (1, 2, 3), Tuple3(0, 0, 0))

    try:
        _ = v - 5
        t.test(False)
    except TypeError:
        t.test(True)

    t.test_section("equality")
    t.test(v == Tuple3(1, 2, 3))
    t.test(u != v)
    t.test(u != "a")

    t.test_section("comparison")
    t.test(not v < (1, 1, 1))
    t.test(v < (2, 3, 4))
    t.test(not v > (2, 3, 4))
    t.test(v <= (1, 2, 3))
    t.test(v >= (1, 2, 3))
    t.test(not v >= (1, 2, 4))
    t.test(v <= (1, 2, 4))
    t.test((1, 2, 4) >= v)

    t.test(min(u, v, Tuple3(0, 0, 0)), (0, 0, 0))
    t.test(max(v, u, v, Tuple3(0, 0, 0)), u)

    t.test_section("hashable")
    t.test_value(hash(v), hash((1, 2, 3)))
