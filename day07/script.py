def solve_part1(positions):
    return min([sum([abs(p0-p) for p0 in positions]) for p in range(max(positions))])


def solve_part2(positions):
    sum_of_int = {0: 0}
    for i in range(1, max(positions)+10):
        sum_of_int[i] = sum_of_int[i-1] + i
    return min([sum([sum_of_int[abs(p0-p)] for p0 in positions]) for p in range(max(positions))])


def parse(input_path):
    with open(input_path, 'r') as f:
        return list(map(int, f.readline().split(',')))


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
