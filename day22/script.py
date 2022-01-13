import re


class Cuboid:
    def __init__(self, op, x1, x2, y1, y2, z1, z2):
        self.op = op
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2

    def intersect(self, c):
        on_x = (self.x1 <= c.x1 <= self.x2) or (c.x1 <= self.x1 <= c.x2)
        on_y = (self.y1 <= c.y1 <= self.y2) or (c.y1 <= self.y1 <= c.y2)
        on_z = (self.z1 <= c.z1 <= self.z2) or (c.z1 <= self.z1 <= c.z2)
        return on_x and on_y and on_z

    def clone(self):
        return Cuboid(self.op, self.x1, self.x2, self.y1, self.y2, self.z1, self.z2)


def exclusion(a, b):
    # return cuboids part of a and not b
    cuboids = []
    if a.x1 < b.x1:
        cuboids.append(Cuboid(a.op, a.x1, b.x1 - 1, a.y1, a.y2, a.z1, a.z2))
        a.x1 = b.x1
    if a.x2 > b.x2:
        cuboids.append(Cuboid(a.op, b.x2 + 1, a.x2, a.y1, a.y2, a.z1, a.z2))
        a.x2 = b.x2
    if a.y1 < b.y1:
        cuboids.append(Cuboid(a.op, a.x1, a.x2, a.y1, b.y1 - 1, a.z1, a.z2))
        a.y1 = b.y1
    if a.y2 > b.y2:
        cuboids.append(Cuboid(a.op, a.x1, a.x2, b.y2 + 1, a.y2, a.z1, a.z2))
        a.y2 = b.y2
    if a.z1 < b.z1:
        cuboids.append(Cuboid(a.op, a.x1, a.x2, a.y1, a.y2, a.z1, b.z1 - 1))
        a.z1 = b.z1
    if a.z2 > b.z2:
        cuboids.append(Cuboid(a.op, a.x1, a.x2, a.y1, a.y2, b.z2 + 1, a.z2))
        a.z2 = b.z2
    return cuboids


def split_cuboids(cuboids):
    res = [cuboids[0]]
    for k in range(1, len(cuboids)):
        next_res = []
        c2 = cuboids[k]
        for c1 in res:
            if not c1.intersect(c2):
                next_res.append(c1)
            else:
                next_res += exclusion(c1.clone(), c2.clone())
        if c2.op == 'on':
            next_res.append(c2)
        res = next_res
    return res


def solve_part2(cuboids):
    split = split_cuboids(cuboids)
    return sum([(c.x2 - c.x1 + 1) * (c.y2 - c.y1 + 1) * (c.z2 - c.z1 + 1) for c in split])


def solve_part1(cuboids):
    return solve_part2([c for c in cuboids
                        if -50 <= c.x1 <= c.x2 <= 50
                        and -50 <= c.y1 <= c.y2 <= 50
                        and -50 <= c.z1 <= c.z2 <= 50])


def parse(input_path):
    regex = r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)'
    actions = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            g = re.match(regex, line.strip()).groups()
            actions.append(Cuboid(g[0], int(g[1]), int(g[2]), int(g[3]), int(g[4]), int(g[5]), int(g[6])))
        return actions


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
