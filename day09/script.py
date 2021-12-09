from collections import deque


def adjacent(P):
    return {(P[0]-1, P[1]), (P[0]+1, P[1]), (P[0], P[1]-1), (P[0], P[1]+1)}


def get_low_points(cave):
    return [P for P in cave if all([(Z not in cave or cave[P] < cave[Z]) for Z in adjacent(P)])]


def solve_part1(cave):
    return sum([cave[P] + 1 for P in get_low_points(cave)])


def basin_size(low, cave):
    seen = set()
    to_check = deque([low])
    while len(to_check):
        P = to_check.popleft()
        if P in seen or P not in cave or cave[P] == 9:
            continue
        seen.add(P)
        for P2 in adjacent(P):
            to_check.append(P2)
    return len(seen)


def solve_part2(cave):
    basins = sorted([basin_size(low, cave) for low in get_low_points(cave)])[::-1]
    return basins[0] * basins[1] * basins[2]


def parse(input_path):
    with open(input_path, 'r') as f:
        cave = {}
        for (i, line) in enumerate(f.readlines()):
            for (j, height) in enumerate(line.strip()):
                cave[(i, j)] = int(height)
        return cave


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
