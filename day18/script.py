LEFT = True
RIGHT = False

class SnailNumber:
    def __init__(self, left=None, right=None, value=None):
        self.left = left
        self.right = right
        self.value = value
        self.parent = None
        
    def clone(self):
        if self.value is None:
            left = self.left.clone()
            right = self.right.clone()
            res = SnailNumber(left, right, None)
            left.parent = res
            right.parent = res
            return res
        else:
            return SnailNumber(None, None, self.value)

    def magnitude(self):
        if self.value is not None:
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def add(self, other):
        result = SnailNumber(self.clone(), other.clone())
        result.left.parent = result
        result.right.parent = result
        result.reduce()
        return result

    def reduce(self):
        while True:
            if self.check_explode(0):
                continue
            if self.check_split():
                continue
            break

    def check_split(self):
        if self.value is None:
            if self.left.check_split():
                return True
            if self.right.check_split():
                return True
        elif self.value > 9:
            self.left = SnailNumber(None, None, self.value // 2)
            self.left.parent = self
            self.right = SnailNumber(None, None, (self.value + 1) // 2)
            self.right.parent = self
            self.value = None
            return True
        else:
            return False

    def check_explode(self, level):
        if self.value is None:
            if self.left.check_explode(level + 1):
                return True
            if self.right.check_explode(level + 1):
                return True
        elif level > 4:
            self.parent.explode()
            return True
        else:
            return False

    def explode(self):
        self.parent.escalate(LEFT, self.left.value, self)
        self.parent.escalate(RIGHT, self.right.value, self)
        self.value = 0
        self.left = self.right = None

    def escalate(self, direction, value, source):
        target = self.left if direction == LEFT else self.right 
        if target == source:
            if self.parent:
                self.parent.escalate(direction, value, self)
        else:
            target.add_exploded_value(not direction, value)

    def add_exploded_value(self, direction, value):
        if self.value is not None:
            self.value += value
        else:
            target = self.left if direction == LEFT else self.right 
            target.add_exploded_value(direction, value)


def create_tree(n):
    if type(n) == int:
        return SnailNumber(None, None, n)
    else:
        return SnailNumber(create_tree(n[0]), create_tree(n[1]))

def link_tree(tree):
    if tree.left:
        tree.left.parent = tree
        link_tree(tree.left)
    if tree.right:
        tree.right.parent = tree
        link_tree(tree.right)


def create_number(n):
    tree = create_tree(n)
    link_tree(tree)
    return tree


def solve_part1(numbers):
    result = numbers[0]
    for snail_number in numbers[1:]:
        result = result.add(snail_number)
    return result.magnitude()

def solve_part2(numbers):
    biggest = 0
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j:
               biggest = max(biggest, numbers[i].add(numbers[j]).magnitude()) 
    return biggest


def parse(input_path):
    with open(input_path, 'r') as f:
        pairs = [eval(l.replace('[', '(').replace(']', ')')) for l in f.readlines()] 
        return list(map(create_number, pairs))


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
