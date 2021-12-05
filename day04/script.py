import re


def make_records(grids):
    records = []
    for i in range(len(grids)):
        record = []
        for j in range(5):
            record.append(set([grids[i][j][k] for k in range(5)]))
            record.append(set([grids[i][k][j] for k in range(5)]))
        records.append(record)
    return records


def score(grid, called):
    return sum([grid[i//5][i % 5] for i in range(25) if grid[i//5][i % 5] not in called]) * called[-1]


def solve_part1(parsed):
    called, grids = parsed
    records = make_records(grids)
    for called_i in range(len(called)):
        for i in range(len(records)):
            for sequence in records[i]:
                sequence.discard(called[called_i])
                if len(sequence) == 0:
                    return score(grids[i], called[:called_i+1])


def solve_part2(parsed):
    called, grids = parsed
    records = make_records(grids)
    won = set()
    for called_i in range(len(called)):
        for i in range(len(records)):
            if i in won:
                continue
            for sequence in records[i]:
                sequence.discard(called[called_i])
                if len(sequence) == 0:
                    won.add(i)
                    if len(won) == len(grids):
                        return score(grids[i], called[:called_i+1])


def parse(input_path):
    with open(input_path, 'r') as f:
        called = list(map(int, f.readline().split(',')))
        grids = []
        grid = []
        for line in f.readlines()[1:]:
            if line.strip() == '':
                grids.append(grid)
                grid = []
            else:
                grid.append(list(map(int, re.split(r' +', line.strip()))))
        grids.append(grid)
        return called, grids


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
