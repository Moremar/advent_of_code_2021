def is_big(cave):
    return cave == cave.upper()


def solve_part1(caves):
    to_process = [('start', {'start'})]
    count = 0
    while len(to_process):
        cave, visited = to_process.pop(0)
        for next_cave in caves[cave]:
            if next_cave == 'end':
                count += 1
            elif is_big(next_cave) or next_cave not in visited:
                to_process.append((next_cave, visited.union({next_cave})))
    return count


def solve_part2(caves):
    to_process = [('start', {'start'}, False)]
    count = 0
    while len(to_process):
        cave, visited, visited_small_twice = to_process.pop(0)
        for next_cave in caves[cave]:
            if next_cave == 'end':
                count += 1
            elif is_big(next_cave) or next_cave not in visited:
                to_process.append((next_cave, visited.union({next_cave}), visited_small_twice))
            elif not visited_small_twice and next_cave != 'start':
                to_process.append((next_cave, visited.union({next_cave}), True))
    return count


def parse(input_path):
    with open(input_path, 'r') as f:
        graph = {}
        for line in f.readlines():
            caves = line.strip().split('-')
            cave1, cave2 = caves[0], caves[1]
            for cave in [cave1, cave2]:
                if cave not in graph:
                    graph[cave] = set()
            graph[cave1].add(cave2)
            graph[cave2].add(cave1)
        return graph


if __name__ == "__main__":
    parsed = parse("sample.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
