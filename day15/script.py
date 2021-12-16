import heapq


def adjacent(p):
    return {(p[0]-1, p[1]), (p[0], p[1]-1), (p[0], p[1]+1), (p[0]+1, p[1])}


def solve_part1(input):
    len_x, len_y, world = input
    risks = {(0, 0): 0}
    to_check = []
    heapq.heappush(to_check, (0, 0, 0))
    while len(to_check):
        risk, x, y = heapq.heappop(to_check)
        for (x_adj, y_adj) in adjacent((x, y)):
            if (x_adj, y_adj) not in world:
                continue
            total_risk = risk + world[(x_adj, y_adj)]
            if (x_adj, y_adj) not in risks or risks[(x_adj, y_adj)] > total_risk:
                risks[(x_adj, y_adj)] = total_risk
                if (x_adj, y_adj) == (len_x - 1, len_y - 1):
                    return total_risk
                heapq.heappush(to_check, (total_risk, x_adj, y_adj))


def make_big_world(len_x, len_y, world):
    bigworld = dict(world)
    for i in range(5):
        for j in range(5):
            for key in world:
                new_i = key[0] + i * len_x
                new_j = key[1] + j * len_y
                new_val = world[key] + i + j
                if world[key] + i + j >= 10:
                    new_val -= 9
                bigworld[(new_i, new_j)] = new_val
    return bigworld


def solve_part2(input):
    len_x, len_y, world = input
    big_world = make_big_world(len_x, len_y, world)
    return solve_part1((len_x * 5, len_y * 5, big_world))


def parse(input_path):
    with open(input_path, 'r') as f:
        world = {}
        for (i, line) in enumerate(f.readlines()):
            for (j, c) in enumerate(line.strip()):
                world[(i, j)] = int(c)
        return i+1, j+1, world


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
