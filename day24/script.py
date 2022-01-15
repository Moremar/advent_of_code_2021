import math

# Brute force takes far too mch time to check
# We analyze what the program does, and notice that it is building
# a bigger and bigger number in register z
# The only way to reduce this number is to choose the input digits carefully
# to set the commands "eql x w" return 1 as often as we can
# Those are used as conditions that reduce z when they are true.
# This leads to a system of equations where Kn is the n-th digit of the MONAD code :
#
#   (1)  K5  = K4 + 7
#   (2)  K6  = K3
#   (3)  K8  = K7 - 4
#   (4)  K9  = K2 + 5
#   (5)  K10 = K1 + 2
#   (6)  K12 = K11 - 6
#   (7)  K14 = K13 + 1
#
# To find the bigger solution, we set all digits to 9 initially and update it to comply
# with each equation :
#    99999999999999
#    99929999999999  (1)
#    99929999999999  (2)
#    99929995999999  (3)
#    94929995999999  (4)
#    74929995999999  (5)
#    74929995999399  (6)
#    74929995999389  (7)
#
# To find the smallest solution, we set all digits to 1 initially and do the same :
#    11111111111111
#    11118111111111  (1)
#    11118111111111  (2)
#    11118151111111  (3)
#    11118151611111  (4)
#    11118151631111  (5)
#    11118151637111  (6)
#    11118151637112  (7)


class Command:
    def __init__(self, op, a, b=None):
        self.op = op
        self.a = a
        self.b = b if b is None or b in 'wxyz' else int(b)

    def __repr__(self):
        return f'{self.op} {self.a} {self.b if self.b is not None else ""}'


class Processor:
    def __init__(self, monad):
        self.mem = {registry : 0 for registry in ['w', 'x', 'y', 'z']}
        self.monad = monad

    def run(self, cmd):
        if cmd.op == 'inp':
            self.mem[cmd.a] = self.monad.pop(0)
        elif cmd.op == 'add':
            val = self.mem[cmd.b] if cmd.b in self.mem else cmd.b
            self.mem[cmd.a] = self.mem[cmd.a] + val
        elif cmd.op == 'mul':
            val = self.mem[cmd.b] if cmd.b in self.mem else cmd.b
            self.mem[cmd.a] = self.mem[cmd.a] * val
        elif cmd.op == 'div':
            val = self.mem[cmd.b] if cmd.b in self.mem else cmd.b
            self.mem[cmd.a] = math.trunc(self.mem[cmd.a] / val)
        elif cmd.op == 'mod':
            val = self.mem[cmd.b] if cmd.b in self.mem else cmd.b
            self.mem[cmd.a] = self.mem[cmd.a] % val
        elif cmd.op == 'eql':
            val = self.mem[cmd.b] if cmd.b in self.mem else cmd.b
            self.mem[cmd.a] = 1 if self.mem[cmd.a] == val else 0

    def __repr__(self):
        return f'[ {self.mem["w"]} {self.mem["x"]} {self.mem["y"]} {self.mem["z"]} ]'


def apply_code(commands, monad):
    processor = Processor([int(c) for c in str(monad)])
    for i, cmd in enumerate(commands):
        processor.run(cmd)
    assert processor.mem['z'] == 0
    return monad


def solve_part1(commands):
    return apply_code(commands, 74929995999389)


def solve_part2(commands):
    return apply_code(commands, 11118151637112)


def parse(input_path):
    with open(input_path, 'r') as f:
        return [Command(*line.split()) for line in f.readlines()]


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
