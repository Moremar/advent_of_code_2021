
def solve_part1(arr):
    return sum([arr[i] < arr[i+1] for i in range(len(arr)-1)])

def solve_part2(arr):
    return solve_part1([arr[i] + arr[i+1] + arr[i+2] for i in range(len(arr)-2)])

def parse(input_path):
    with open(input_path, 'r') as f:
        return list(map(int, f.readlines()))

if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
