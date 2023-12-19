import typing


class Range:
    def __init__(self, start, end):
        """Create a range instance [start, end>."""
        self._start = start
        self._end = end

    def __contains__(self, item):
        """Check if an item is in the range."""
        return self._start <= item < self._end

    def __repr__(self):
        """Return the representation of this range."""
        return f"Range({self._start}, {self._end})"

    def overlap(self, other: typing.Self) -> typing.Self:
        """Return the overlap between two ranges."""
        if self._start in other:
            return Range(self._start, min(self._end, other._end))
        elif self._end in other:
            return Range(max(self._start, other._start), self._end)
        elif self._start <= other._start and other._end <= self._end:
            return Range(other._start, other._end)
        elif other._start <= self._start and self._end <= other._end:
            return Range(self._start, self._end)
        else:
            return None

    def __lt__(self, other: typing.Self) -> bool:
        """Check if this range is less than another.

        Start of this range is less than the start of the other range.
        """
        return self._start < other._start

    def __eq__(self, other: typing.Self) -> bool:
        """Check if this range is equal to another."""
        return self._start == other._start and self._end == other._end

    def __hash__(self) -> int:
        """Hash this range."""
        return hash((self._start, self._end))

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def __len__(self) -> int:
        """Return the length of the range."""
        return self._end - self._start


if __name__ == '__main__':
    r1 = Range(0, 10)
    assert 9 in r1
    assert 0 in r1
    assert 5 in r1
    assert 10 not in r1
    assert -1 not in r1

    r2 = Range(5, 15)

    assert r1.overlap(r2) == Range(5, 10)

    r3 = Range(-5, 0)
    assert r1.overlap(r3) is None

    assert r1 < r2
    assert r2 > r1
    assert r1 == r1
    assert r1 != r2
    assert r1 != r3
    assert r2 != r3
    assert r3 != r1
    assert r3 < r1
    assert not r3 > r1

    assert hash(r1.overlap(r2)) == hash(Range(5, 10))

    assert len(r1) == 10
    assert len(r2) == 10
    assert len(r3) == 5
