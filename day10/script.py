MATCHING = { '(': ')', '[': ']', '{': '}', '<': '>' }
SCORE_1  = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
SCORE_2  = { ')': 1, ']': 2, '}': 3, '>': 4 }


def check(command):
    s = ''
    for c in command:
        if c in MATCHING:
            s += c
        elif len(s) > 0 and c == MATCHING[s[-1]]:
            s = s[:-1]
        else:
            return c


def solve_part1(commands):
    return sum([SCORE_1[c] for c in [check(command) for command in commands] if c is not None])


def missing(command):
    s = ''
    for c in command:
        if c in MATCHING:
            s += c
        else:
            s = s[:-1]
    return ''.join([MATCHING[c] for c in s[::-1]])


def missing_score(missing):
    score = 0
    for c in missing:
        score = 5 * score + SCORE_2[c]
    return score


def solve_part2(commands):
    valid_commands = [command for command in commands if check(command) is None]
    return sorted([missing_score(missing(command)) for command in valid_commands])[len(valid_commands)//2]


def parse(input_path):
    with open(input_path, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
