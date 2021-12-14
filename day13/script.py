def fold_paper(dots, fold):
    next_dots = set()
    for dot in dots:
        if fold[0] == 'x' and dot[0] > fold[1]:
            next_dot = (fold[1] - (dot[0] - fold[1]), dot[1])
        elif fold[0] == 'y' and dot[1] > fold[1]:
            next_dot = (dot[0], fold[1] - (dot[1] - fold[1]))
        else:
            next_dot = dot
        next_dots.add(next_dot)
    return next_dots


def solve_part1(input):
    dots, folds = input
    return len(fold_paper(dots, folds[0]))


def get_image(dots, x_max, y_max):
    image = '\n'
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            image += '* ' if (x, y) in dots else '  '
        image += '\n'
    return image


def solve_part2(input):
    dots, folds = input
    for fold in folds:
        dots = fold_paper(dots, fold)
    return get_image(dots, max([x for (x, y) in dots]) + 1, max([y for (x, y) in dots]) + 1)


def parse(input_path):
    with open(input_path, 'r') as f:
        dots = set()
        folds = []
        for line in f.readlines():
            if ',' in line:
                dots.add(tuple(map(int, line.split(','))))
            elif '=' in line:
                folds.append(('x' if 'x' in line else 'y', int(line.split('=')[-1])))
        return dots, folds


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
