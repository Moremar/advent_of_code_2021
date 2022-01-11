def enhanced_number(image, i, j, default):
    s = ''
    for x in range(i-1, i+2):
        for y in range(j - 1, j + 2):
            val = image[(x, y)] if (x, y) in image else default
            s += '1' if val == '#' else '0'
    return int(s, 2)


def enhance(image, algo, default):
    min_i = min([i for (i, _) in image])
    max_i = max([i for (i, _) in image])
    min_j = min([j for (_, j) in image])
    max_j = max([j for (_, j) in image])
    enhanced_image = {}
    for i in range(min_i-2, max_i+3):
        for j in range(min_j - 2, max_j + 3):
            number = enhanced_number(image, i, j, default)
            enhanced_image[(i, j)] = algo[number]
    return enhanced_image


def repeat_enhance(data, times):
    algo, image = data
    for k in range(times):
        default = '#' if algo[0] == '#' and k % 2 == 1 else '.'
        image = enhance(image, algo, default)
    return len([1 for (x, y) in image if image[(x, y)] == '#'])


def solve_part1(data):
    return repeat_enhance(data, 2)


def solve_part2(data):
    return repeat_enhance(data, 50)


def parse(input_path):
    with open(input_path, 'r') as f:
        algo = f.readline().strip()
        f.readline()
        image = {}
        for (i, line) in enumerate(f.readlines()):
            for (j, c) in enumerate(line):
                image[(i, j)] = c
        return algo, image


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
