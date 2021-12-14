from collections import Counter
import re


def evolve(polymer, formulas):
    res = polymer[0]
    for i in range(len(polymer)-1):
        res += formulas[polymer[i:i+2]] + polymer[i+1]
    return res


def solve_part1(input):
    polymer, formulas = input
    for _ in range(10):
        polymer = evolve(polymer, formulas)
    count = Counter(polymer).most_common()
    return count[0][1] - count[-1][1]


# 40 steps is too big to run it iteratively.
# Instead we will :
#  - Run 20 steps for each possible pair of elements and store the generated polymer
#    and the number of each elements in it
#  - Iterate through the generated polymer after 20 steps for each element of the initial
#    polymer, and for each element of it we add the number of elements to a counter
#    after another 20 steps (no need to calculate it, already stored in previous step)
# Note : that function is still pretty slow, it takes ~8min to complete 
def solve_part2(input):
    init_polymer, formulas = input
    after_20 = {}
    after_40 = {}
    # polymer and count for each pair after 20 iterations
    for formula in formulas:
        polymer = formula
        for _ in range(20):
            polymer = evolve(polymer, formulas)
        after_20[formula] = Counter(polymer), polymer
    # count for each pair after 40 iterations
    for formula in formulas:
        counter = Counter()
        for i in range(len(after_20[formula][1]) - 1):
            counter += after_20[after_20[formula][1][i:i+2]][0]
            if i > 0:
                counter[after_20[formula][1][i]] -= 1
        after_40[formula] = counter
    # sum counters after 40 iterations for each pair in the initial polymer
    counter = Counter()
    for i in range(len(init_polymer)-1):
        counter += after_40[init_polymer[i:i+2]]
        if i > 0:
            counter[init_polymer[i]] -= 1
    count = counter.most_common()
    return count[0][1] - count[-1][1]


def parse(input_path):
    with open(input_path, 'r') as f:
        polymer = f.readline().strip()
        f.readline()
        formulas = {}
        for line in f.readlines():
            left, right = re.match(r'([A-Z]+) -> ([A-Z]+)', line).groups()
            formulas[left] = right
        return polymer, formulas


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
