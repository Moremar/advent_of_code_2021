import re


def solve(vents, diagonal):
    points = {}
    for (x1, y1), (x2, y2) in vents:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2)+1):
                points[(x1, y)] = points[(x1, y)] + 1 if (x1, y) in points else 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                points[(x, y1)] = points[(x, y1)] + 1 if (x, y1) in points else 1
        elif diagonal:
            if x1 > x2:
                (x1, y1), (x2, y2) = (x2, y2), (x1, y1)
            for i, x in enumerate(range(x1, x2 + 1)):
                y = y1 + i if y1 < y2 else y1 - i
                points[(x, y)] = points[(x, y)] + 1 if (x, y) in points else 1
    return len([p for p in points if points[p] > 1])


def solve_part1(vents):
    return solve(vents, False)


def solve_part2(vents):
    return solve(vents, True)


def parse(input_path):
    with open(input_path, 'r') as f:
        vents = []
        for line in f.readlines():
            x1, y1, x2, y2 = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line).groups()
            vents.append(((int(x1), int(y1)), (int(x2), int(y2))))
        return vents


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
