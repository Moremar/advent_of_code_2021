
DIGITS = {
    0: {'a', 'b', 'c', 'e', 'f', 'g'},
    1: {'c', 'f'},
    2: {'a', 'c', 'd', 'e', 'g'},
    3: {'a', 'c', 'd', 'f', 'g'},
    4: {'b', 'c', 'd', 'f'},
    5: {'a', 'b', 'd', 'f', 'g'},
    6: {'a', 'b', 'd', 'e', 'f', 'g'},
    7: {'a', 'c', 'f'},
    8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
    9: {'a', 'b', 'c', 'd', 'f', 'g'}
}

LETTERS = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}


def solve_part1(rows):
    return sum([len([o for o in rows[i][1] if len(o) in [2,3,4,7]]) for i in range(len(rows))])


def get_segment_mapping(inputs):
    mapping = {i: set(LETTERS) for i in LETTERS}
    for segments in inputs:
        possibly_on = set()
        possibly_off = set()
        for digit in DIGITS:
            if len(DIGITS[digit]) == len(segments):
                possibly_on = possibly_on.union(DIGITS[digit])
                possibly_off = possibly_off.union(LETTERS.difference(DIGITS[digit]))
        for segment in segments:
            mapping[segment] = mapping[segment].intersection(possibly_on)
        for segment in LETTERS.difference(segments):
            mapping[segment] = mapping[segment].intersection(possibly_off)
    for i in mapping:
        if len(mapping[i]) == 1:
            for j in mapping:
                if j != i:
                    mapping[j] = mapping[j].difference(mapping[i])
    return {i: next(iter(mapping[i])) for i in mapping}


def solve_row(row):
    mapping = get_segment_mapping(row[0])
    res = 0
    for segments in row[1]:
        for i in DIGITS:
            if {mapping[s] for s in segments} == DIGITS[i]:
                res = 10 * res + i
                break
    return res


def solve_part2(rows):
    return sum([solve_row(r) for r in rows])


def parse(input_path):
    with open(input_path, 'r') as f:
        res = []
        for line in f.readlines():
            input, output = line.strip().split(' | ')
            res.append((input.split(), output.split()))
        return res


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
