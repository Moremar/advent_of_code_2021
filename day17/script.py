import re


def trajectory(x0, y0, target):
    x1, x2, y1, y2 = target
    x, y = x0, y0
    max_y = 0
    pos = (0, 0)
    while True:
        pos = (pos[0] + x, pos[1] + y)
        if pos[1] > max_y:
            max_y = pos[1]
        if pos[0] > x2 or pos[1] < y1:
            return False, max_y
        if pos[0] >= x1 and pos[1] <= y2:
            return True, max_y
        x = max(0, x-1) 
        y -= 1 


def solve_part1(target):
    best_summit = 0
    for y in range(1, 1000):
        for x in range(1, 1000):
            hit_target, summit = trajectory(x, y, target) 
            if hit_target:
                best_summit = summit
                break # all trajectories with the same y go to the same height
    return best_summit


def solve_part2(target):
    valid_shots = 0
    for y in range(-1000, 1000):
        for x in range(1, 1000):
            hit_target, summit = trajectory(x, y, target) 
            if hit_target:
                valid_shots += 1
    return valid_shots


def parse(input_path):
    with open(input_path, 'r') as f:
        pattern = r'target area: x=(-*\d+)..(-*\d+), y=(-*\d+)..(-*\d+)'
        x1, x2, y1, y2 = re.match(pattern, f.readline().strip()).groups()
        return int(x1), int(x2), int(y1), int(y2)


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
