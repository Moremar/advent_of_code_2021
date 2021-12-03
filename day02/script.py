
def solve_part1(moves):
    x, y = 0, 0
    for move in moves:
        x += move[1] if move[0] == 'forward' else 0
        y += move[1] if move[0] == 'down' else -move[1] if move[0] == 'up' else 0
    return x * y


def solve_part2(moves):
    x, y, aim = 0, 0, 0
    for move in moves:
        aim += move[1] if move[0] == 'down' else -move[1] if move[0] == 'up' else 0
        x += move[1] if move[0] == 'forward' else 0
        y += move[1] * aim if move[0] == 'forward' else 0
    return x * y


def parse(input_path):
    with open(input_path, 'r') as f:
        return [(l[:l.index(' ')], int(l[l.index(' '):])) for l in f.readlines()]


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
