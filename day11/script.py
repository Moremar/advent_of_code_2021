
def adjacent(p):
    return {(p[0]-1, p[1]-1), (p[0]-1, p[1]), (p[0]-1, p[1]+1),
            (p[0], p[1]-1), (p[0], p[1]+1),
            (p[0]+1, p[1]-1), (p[0]+1, p[1]), (p[0]+1, p[1]+1)}


def next_state(octopus):
    flashed = set()
    next_octopus = {(x, y): octopus[(x, y)] + 1 for (x, y) in octopus}
    modified = True
    while modified:
        modified = False
        for (x, y) in next_octopus:
            if next_octopus[(x,y)] > 9 and (x, y) not in flashed:
                flashed.add((x, y))
                for (i, j) in adjacent((x, y)):
                    if (i, j) in next_octopus:
                        next_octopus[(i, j)] = next_octopus[(i, j)] + 1
                modified = True
    for (x, y) in flashed:
        next_octopus[(x, y)] = 0
    return next_octopus, len(flashed)


def solve_part1(octopus):
    total_flashed = 0
    for i in range(100):
        octopus, flashed = next_state(octopus)
        total_flashed += flashed
    return total_flashed


def solve_part2(octopus):
    i = 0
    while True:
        i += 1
        octopus, flashed = next_state(octopus)
        if flashed == len(octopus):
            return i


def parse(input_path):
    with open(input_path, 'r') as f:
        octopus = {}
        for (i, line) in enumerate(f.readlines()):
            for (j, energy) in enumerate(line.strip()):
                octopus[(i, j)] = int(energy)
        return octopus


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
