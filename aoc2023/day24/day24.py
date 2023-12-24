import typing

import aoc
import sympy

tester = aoc.Tester("Never Tell Me The Odds")


class Particle:
    def __init__(self, pos: tuple[int, int, int], vel: tuple[int, int, int]):
        self._pos = pos
        self._vel = vel

    @property
    def x(self) -> int:
        return self._pos[0]

    @property
    def y(self) -> int:
        return self._pos[1]

    @property
    def z(self) -> int:
        return self._pos[2]

    @property
    def dx(self) -> int:
        return self._vel[0]

    @property
    def dy(self) -> int:
        return self._vel[1]

    @property
    def dz(self) -> int:
        return self._vel[2]

    def tick(self, t: int = 1) -> typing.Self:
        return Particle(
            (self.x + self.dx * t, self.y + self.dy * t, self.z + self.dz * t), self._vel
        )

    def __eq__(self, other: typing.Self) -> bool:
        # check if the particles are at the same position
        return self._pos == other._pos


    def intersect_vectors_2d(
        self, other: typing.Self, allow_past: bool = False
    ) -> tuple[float, float, float]:
        dx = other.x - self.x
        dy = other.y - self.y
        det = self.dy * other.dx - self.dx * other.dy
        if det == 0:
            # parallel
            # print(f"det={det}")
            # print(f"parallel self={self} other={other}")
            return None
        u = (dy * other.dx - dx * other.dy) / det
        v = (dy * self.dx - dx * self.dy) / det

        if not allow_past and u < 0 or v < 0:
            # in the past
            # print(f"u={u}, v={v}")
            return None

        m0 = self.dy / self.dx
        m1 = other.dy / other.dx
        b0 = self.y - m0 * self.x
        b1 = other.y - m1 * other.x

        if m0 == m1:
            print(f"m0={m0}, m1={m1}")
            return None

        x = (b1 - b0) / (m0 - m1)
        y = m0 * x + b0

        return (
            x,
            y,
            v,  # time of intersection for self
        )

    def distance(self) -> int:
        return abs(self._pos[0]) + abs(self._pos[1]) + abs(self._pos[2])

    def __repr__(self):
        return f"Particle(pos={self._pos}, vel={self._vel})"


def parse(data: str) -> list[Particle]:
    poses = set()
    particles = []
    for line in data.splitlines():
        pos, vel = line.split("@")
        pos = tuple(map(int, pos.split(",")))
        if pos in poses:
            print(f"Duplicate position: {pos}")
        poses.add(pos)
        vel = tuple(map(int, vel.split(",")))
        particles.append(Particle(pos, vel))
    return particles


def intersect_2d(
    particles: list[Particle], minimum: int, maximum: int
) -> list[tuple[Particle, Particle, tuple[float, float, float]]]:
    intersections = []
    for j in range(len(particles) - 1):
        for i in range(j + 1, len(particles)):
            p = particles[i]
            q = particles[j]
            if p != q:
                intersect = p.intersect_vectors_2d(q)

                if intersect is None:
                    continue

                if minimum <= intersect[0] <= maximum and minimum <= intersect[1] <= maximum:
                    intersections.append((p, q, intersect))

    return intersections


def smash(particles: list[Particle]) -> int:
    x = sympy.Symbol("x")
    y = sympy.Symbol("y")
    z = sympy.Symbol("z")
    symbols = [x, y, z]
    sympy.init_printing(use_unicode=True)
    symbols.append(sympy.Symbol("dx dy dz"))
    eqs = []
    for i, p in enumerate(particles[:3]):
        symbols.append(sympy.Symbol(f"t{i}"))
        eqs.append(sympy.sympify(f"{p.x} + {p.dx} * t{i} - x - dx * t{i}"))
        eqs.append(sympy.sympify(f"{p.y} + {p.dy} * t{i} - y - dy * t{i}"))
        eqs.append(sympy.sympify(f"{p.z} + {p.dz} * t{i} - z - dz * t{i}"))

    result = sympy.solve(eqs)[0]
    return int(result[x] + result[y] + result[z])


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    particles = parse(aoc.read_input("input_test"))

    intersections = intersect_2d(particles, 7, 27)
    t.test_value(len(intersections), 2)

    t.test_value(smash(particles), 47)


run_tests(tester)

data = aoc.read_input()
particles = parse(data)

tester.test_section("Part 1")
intersections = intersect_2d(particles, 200000000000000, 400000000000000)
solution_1 = len(intersections)
tester.test_solution(solution_1, 16172)

tester.test_section("Part 2")
solution_2 = smash(particles)
tester.test_solution(solution_2, 600352360036779)
