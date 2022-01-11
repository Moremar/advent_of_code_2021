import re


def beacon_orientations(beacon):
    x, y, z = beacon
    return [
        (x, y, z), (-y, x, z), (-x, -y, z), (y, -x, z),      # original orientation
        (x, -z, y), (z, x, y), (-x, z, y), (-z, -x, y),      # flip y to z by 90 deg
        (x, -y, -z), (y, x, -z), (-x, y, -z), (-y, -x, -z),  # flip y to z by 180 deg
        (x, z, -y), (-z, x, -y), (-x, -z, -y), (z, -x, -y),  # flip y to z by -90 deg deg
        (-z, y, x), (-y, -z, x), (z, -y, x), (y, z, x),      # flip x to z by 90 deg
        (z, y, -x), (-y, z, -x), (-z, -y, -x), (y, -z, -x)   # flip x to z by -90 deg
    ]


def manhattan(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2]) 


class Scanner:
    def __init__(self, scanner_id, beacons):
        self.scanner_id = scanner_id
        self.beacons = beacons
        self.fixed = False
        self.position = (0, 0, 0)

    def orientations(self):
        return zip(*[beacon_orientations(beacon) for beacon in self.beacons])

    def overlap(self, fixed_scanner):
        for beacons in self.orientations():
            # try to find a common translation between beacons of the 2 scanners
            translations = {}
            for (x, y, z) in beacons:
                for (fx, fy, fz) in fixed_scanner.beacons:
                    diff = (fx-x, fy-y, fz-z)
                    if diff not in translations:
                        translations[diff] = 0
                    translations[diff] += 1
                    if translations[diff] == 12:
                        fp = fixed_scanner.position
                        self.position = fp[0] + diff[0], fp[1] + diff[1], fp[2] + diff[2]
                        self.beacons = beacons
                        self.fixed = True
                        return True
        return False


def fix_scanners(scanners):
    scanners[0].fixed = True
    fixed = { scanners[0].scanner_id }
    while len(fixed) < len(scanners):
        for scanner in scanners:
            if scanner.scanner_id not in fixed:
                for fixed_scanner_id in fixed:
                    if scanner.overlap(scanners[fixed_scanner_id]):
                        fixed.add(scanner.scanner_id)
                        break


def solve_part1(scanners):
    fix_scanners(scanners)
    beacons = set()
    for scanner in scanners:
        for (x, y, z) in scanner.beacons:
            (dx, dy, dz) = scanner.position
            beacons.add((x+dx, y+dy, z+dz))
    return len(beacons)


def solve_part2(scanners):
    fix_scanners(scanners)
    max_manhattan = 0
    for s1 in scanners:
        for s2 in scanners:
            if s1 is not s2:
                max_manhattan = max(max_manhattan, manhattan(s1.position, s2.position))
    return max_manhattan


def parse(input_path):
    with open(input_path, 'r') as f:
        scanners = []
        for line in f.readlines():
            if '--' in line:
                scanner_id = int(re.match(r'--- scanner (\d+) ---', line).group(1))
                beacons = []
            elif len(line.strip()) > 0:
                x, y, z = re.match(r'(-?\d+),(-?\d+),(-?\d+)', line).groups()
                beacons.append((int(x), int(y), int(z)))
            else:
                scanners.append(Scanner(scanner_id, beacons))
        scanners.append(Scanner(scanner_id, beacons))
        return scanners


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))