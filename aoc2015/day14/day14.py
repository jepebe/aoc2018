from dataclasses import dataclass

import intcode as ic


@dataclass
class Reindeer:
    name: str
    speed: int = 0  # km/s
    stamina: int = 0  # seconds
    rest: int = 0  # seconds
    distance: int = 0  # km
    score: int = 0

    _resting = 0
    _stamina = None

    def clock(self, ticks=1):
        if self._stamina is None:
            self._stamina = self.stamina

        for i in range(ticks):
            if self._resting > 0:
                self._resting -= 1
                if self._resting == 0:
                    self._stamina = self.stamina
            elif self._stamina > 0:
                self.distance += self.speed
                self._stamina -= 1
                if self._stamina == 0:
                    self._resting = self.rest


def parse_reindeer(lines):
    reindeer = []
    for line in lines:
        line = line.replace('can fly ', '')
        line = line.replace(' km/s for', '')
        line = line.replace(' seconds, but then must rest for', '')
        line = line.replace(' seconds.', '')
        name, speed, stamina, rest = line.split()
        reindeer.append(Reindeer(name, int(speed), int(stamina), int(rest)))
    return reindeer


def race(reindeer, ticks=1000):
    for i in range(ticks):
        max_distance = 0
        for deer in reindeer:
            deer.clock()
            if deer.distance > max_distance:
                max_distance = deer.distance

        for deer in reindeer:
            if deer.distance == max_distance:
                deer.score += 1


tester = ic.Tester('Reindeer Olympics')

comet = Reindeer('Comet', 14, 10, 127)
dancer = Reindeer('Dancer', 16, 11, 162)
race([comet, dancer])
tester.test_value(comet.score, 312)
tester.test_value(dancer.score, 689)
tester.test_value(comet.distance, 1120)
tester.test_value(dancer.distance, 1056)

with open('input') as f:
    lines = f.readlines()

reindeer = parse_reindeer(lines)
race(reindeer, 2503)

max_reindeer_distance = max(reindeer, key=lambda r: r.distance)
max_reindeer_score = max(reindeer, key=lambda r: r.score)

tester.test_value(max_reindeer_distance.distance, 2640, 'solution to exercise 1 = %s')
tester.test_value(max_reindeer_score.score, 1102, 'solution to exercise 2 = %s')
