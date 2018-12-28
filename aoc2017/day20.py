def distance(pos):
    return abs(pos[0]) + abs(pos[1]) + abs(pos[2])


def parse_value(particle):
    x, y, z = map(int, particle[3:-1].split(','))
    return x, y, z


def parse_particles(lines):
    particles = []

    for line in lines:
        p, v, a = line.split(', ')

        p = parse_value(p.strip())
        v = parse_value(v.strip())
        a = parse_value(a.strip())

        particles.append({
            'p': p,
            'v': v,
            'a': a,
            'd': distance(p)
        })

    return particles


def simulate(particles, remove_collisons=False):
    min_particle = 0

    for i, p in enumerate(particles):
        pos = p['p']
        vel = p['v']
        acl = p['a']

        vel = vel[0] + acl[0], vel[1] + acl[1], vel[2] + acl[2]
        pos = pos[0] + vel[0], pos[1] + vel[1], pos[2] + vel[2]

        p['p'] = pos
        p['v'] = vel
        p['d'] = distance(pos)

        if p['d'] < particles[min_particle]['d']:
            min_particle = i

    pos = {}
    for i, particle in enumerate(particles):
        p = particle['p']

        if p not in pos:
            pos[p] = []
        pos[p].append(i)

    collided = []
    for ps in pos.values():
        if len(ps) > 1:
            for cs in ps:
                collided.append(particles[cs])

    collison_count = len(collided)

    if remove_collisons:
        for collison in collided:
            particles.remove(collison)

    #print(min_particle, collison_count)

    return min_particle, collison_count


if __name__ == '__main__':
    p = [
        {'p': (3, 0, 0),
         'v': (2, 0, 0),
         'a': (-1, 0, 0),
         'd': 3
         },
        {'p': (4, 0, 0),
         'v': (0, 0, 0),
         'a': (-2, 0, 0),
         'd': 4
         }
    ]

    assert simulate(p) == (1, 0)
    assert p[0]['d'] == 4
    assert p[1]['d'] == 2
    assert simulate(p) == (1, 0)
    assert p[0]['d'] == 4
    assert p[1]['d'] == 2
    assert simulate(p) == (0, 0)
    assert p[0]['d'] == 3
    assert p[1]['d'] == 8

    with open('day20_test.txt', 'r') as f:
        lines = f.read().splitlines(keepends=False)

    p = parse_particles(lines)
    assert simulate(p, True) == (2, 0)
    assert simulate(p, True) == (0, 3)
    assert simulate(p, True) == (0, 0)


    with open('day20.txt', 'r') as f:
        lines = f.read().splitlines(keepends=False)

    p = parse_particles(lines)

    for i in range(1000):
        min_particle = simulate(p)
    print(min_particle, len(p))

    p = parse_particles(lines)
    for i in range(1000):
        min_particle = simulate(p, True)
    print(min_particle, len(p))



