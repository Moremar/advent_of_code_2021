
def epsilon(arr):
    return [int(sum([arr[j][i] for j in range(len(arr))]) < len(arr) // 2) for i in range(len(arr[0]))]


def gamma(arr):
    return [1 - i for i in epsilon(arr)]


def decimal(arr):
    return sum([arr[i] * 2**(len(arr)-i-1) for i in range(len(arr))])


def rating(arr, oxygen):
    pool = list(arr)
    i = 0
    while len(pool) > 1:
        count = sum([pool[j][i] for j in range(len(pool))])
        bit = (count >= len(pool) - count) if oxygen else (count < len(pool) - count)
        pool = [p for p in pool if p[i] == bit]
        i += 1
    return pool[0]


def solve_part1(arr):
    return decimal(gamma(arr)) * decimal(epsilon(arr))


def solve_part2(arr):
    return decimal(rating(arr, True)) * decimal(rating(arr, False))


def parse(input_path):
    with open(input_path, 'r') as f:
        res = []
        for line in f.readlines():
            res.append(tuple(map(int, list(line.strip()))))
        return res


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
