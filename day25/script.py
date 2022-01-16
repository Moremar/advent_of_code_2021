
def get_next_state(world):
    max_i = max([i for (i, _) in world])
    max_j = max([j for (_, j) in world])
    # move all cucumbers moving east
    moved_east = {}
    for i in range(max_i+1):
        for j in range(max_j+1):
            if (i, j) in moved_east:
                continue
            prev_j = (j-1 + (max_j+1)) % (max_j + 1)
            if world[i, j] == '.' and world[i, prev_j] == '>':
                moved_east[i, j] = '>'
                moved_east[i, prev_j] = '.'
            else:
                moved_east[i, j] = world[i, j]
    # move all cucumbers moving south
    moved_south = {}
    for i in range(max_i + 1):
        for j in range(max_j + 1):
            if (i, j) in moved_south:
                continue
            prev_i = (i - 1 + (max_i + 1)) % (max_i + 1)
            if moved_east[i, j] == '.' and moved_east[prev_i, j] == 'v':
                moved_south[i, j] = 'v'
                moved_south[prev_i, j] = '.'
            else:
                moved_south[i, j] = moved_east[i, j]
    return moved_south


def solve_part1(world):
    steps = 0
    while True:
        steps += 1
        next_state = get_next_state(world)
        if world == next_state:
            return steps
        world = next_state


def parse(input_path):
    with open(input_path, 'r') as f:
        world = {}
        for (i, line) in enumerate(f.readlines()):
            for (j, c) in enumerate(line.strip()):
                world[i, j] = c
        return world


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
