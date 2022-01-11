import functools


class Dice:
    def __init__(self):
        self.last_val = 0
        self.called = 0

    def next_val(self):
        self.called += 1
        self.last_val += 1
        if self.last_val > 100:
            self.last_val -= 100
        return self.last_val


def solve_part1(data):
    scores = [0, 0]
    positions = [data[0] - 1, data[1] - 1]
    next_player = 0
    dice = Dice()
    while scores[0] < 1000 and scores[1] < 1000:
        dice_sum = sum([dice.next_val() for _ in range(3)])
        positions[next_player] += dice_sum
        positions[next_player] %= 10
        scores[next_player] += positions[next_player] + 1
        next_player = (next_player + 1) % 2
    return dice.called * min(scores)


@functools.cache
def calculate(pos1, pos2, score1, score2, player):
    if score1 >= 21:
        return (1, 0)
    elif score2 >= 21:
        return (0, 1)
    states = []
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                dice_sum = i + j + k
                if player == 0:
                    new_pos1 = (pos1 + dice_sum) % 10
                    new_score1 = score1 + new_pos1 + 1
                    states.append((new_pos1, pos2, new_score1, score2, 1))
                else:
                    new_pos2 = (pos2 + dice_sum) % 10
                    new_score2 = score2 + new_pos2 + 1
                    states.append((pos1, new_pos2, score1, new_score2, 0))
    scores = [calculate(*state) for state in states]
    return sum([score[0] for score in scores]), sum([score[1] for score in scores])


def solve_part2(data):
    return max(calculate(data[0] - 1, data[1] - 1, 0, 0, 0))


def parse(input_path):
    with open(input_path, 'r') as f:
        player0 = int(f.readline().split(':')[1])
        player1 = int(f.readline().split(':')[1])
        return player0, player1


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
