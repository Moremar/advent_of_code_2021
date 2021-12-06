
def generated_per_next_split(max_day):
    # generate a table saying how many lanternfish result from a lanternfish
    # which next split is on a given day
    table = {}
    for i in range(max_day+10, 0, -1):
        table[i] = 1 if i >= max_day else (table[i+7] + table[i+9])
    return table


def solve(next_splits, max_day):
    table = generated_per_next_split(max_day)
    return sum([table[next_split] for next_split in next_splits])


def parse(input_path):
    with open(input_path, 'r') as f:
        return list(map(int, f.readline().split(',')))


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve(parsed, 80))
    print('Part 2 :', solve(parsed, 256))
