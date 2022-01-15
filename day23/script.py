import heapq

energy_map = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
rooms_col = {'A': 3, 'B': 5, 'C': 7, 'D': 9}


class HeapWorld:
    def __init__(self, energy, world):
        self.energy = energy
        self.world = world

    # must define __lt__() so it can be used in the heapq
    def __lt__(self, other):
        return self.energy < other.energy


def is_final(world):
    first_2_rows = world[2, 3] == world[3, 3] == 'A' \
                   and world[2, 5] == world[3, 5] == 'B' \
                   and world[2, 7] == world[3, 7] == 'C' \
                   and world[2, 9] == world[3, 9] == 'D'
    last_2_rows = (5, 3) in world \
                  and world[4, 3] == world[5, 3] == 'A' \
                  and world[4, 5] == world[5, 5] == 'B' \
                  and world[4, 7] == world[5, 7] == 'C' \
                  and world[4, 9] == world[5, 9] == 'D'
    return first_2_rows if (5, 3) not in world else (first_2_rows and last_2_rows)


def draw(world):
    image = ''
    for x in range(1, 6 if (5, 3) in world else 4):
        for y in range(1, 12):
            image += world[(x, y)] if (x, y) in world else ' '
        image += '\n'
    return image


def adjacent(p):
    return {(p[0], p[1] - 1), (p[0], p[1] + 1), (p[0] - 1, p[1]), (p[0] + 1, p[1])}


def move_to_rooms(initial_distance, world):
    # move all amphipods with a clear path to their destination room
    for (x, y) in world:
        if world[x, y] not in 'ABCD':
            continue

        reachable = {(x, y)}
        to_check = [(0, x, y)]
        while len(to_check):
            (distance, i, j) = to_check.pop(0)
            for adj_coord in adjacent((i, j)):
                if adj_coord not in world or world[adj_coord] != '.' or adj_coord in reachable:
                    continue
                if adj_coord[0] > 1:
                    in_good_room = adj_coord[1] == rooms_col[world[(x, y)]]
                    if distance == 0 or not in_good_room:
                        # it may be getting out from an incorrect initial room
                        reachable.add(adj_coord)
                        to_check.append((distance + 1, *adj_coord))
                        continue

                    below1 = (adj_coord[0] + 1, adj_coord[1])
                    below2 = (adj_coord[0] + 2, adj_coord[1])
                    below3 = (adj_coord[0] + 3, adj_coord[1])
                    if below1 in world and world[below1] == '.':
                        # not yet at the bottom of the room
                        reachable.add(adj_coord)
                        to_check.append((distance + 1, *adj_coord))
                        continue

                    valid_below = (below1 not in world or world[below1] in [world[(x, y)]]) \
                                  and (below2 not in world or world[below2] in [world[(x, y)]]) \
                                  and (below3 not in world or world[below3] in [world[(x, y)]])
                    if valid_below:
                        # can reach the deepest available spot of the room, perform the move
                        next_world = dict(world)
                        next_world[(x, y)], next_world[adj_coord] = next_world[adj_coord], next_world[(x, y)]
                        energy = energy_map[world[(x, y)]] * (distance + 1)
                        return move_to_rooms(initial_distance + energy, next_world)
                else:
                    reachable.add(adj_coord)
                    to_check.append((distance + 1, *adj_coord))
    # no change if no amphipod can go to its room
    return initial_distance, world


def next_worlds_after_move(world, coord):
    # get the list of next world states after moving the amphipod on a given position
    c = world[coord]
    valid_moves = set()
    seen = {coord}
    to_check = [(0, coord)]

    while len(to_check):
        distance, curr_coord = to_check.pop(0)
        for adj_coord in adjacent(curr_coord):
            if adj_coord not in world or world[adj_coord] != '.' or adj_coord in seen:
                continue
            seen.add(adj_coord)
            to_check.append((distance + 1, adj_coord))
            if adj_coord[0] > 1:
                # not allowed to go in a room, all moves to rooms are done automatically
                # when possible after a valid move by apply_obvious_moves()
                continue
            # can go to the corridor only if coming from a room
            if coord[0] > 1 and adj_coord[1] not in {3, 5, 7, 9}:
                valid_moves.add((distance + 1, adj_coord))

    next_worlds = []
    for valid_move in valid_moves:
        next_world = dict(world)
        distance, next_coord = valid_move
        next_world[coord], next_world[next_coord] = next_world[next_coord], next_world[coord]
        next_worlds.append(move_to_rooms(energy_map[c] * distance, next_world))

    return next_worlds


def get_next_worlds(world):
    next_worlds = []
    for coord in world:
        c = world[coord]
        if c not in 'ABCD':
            continue
        below1 = (coord[0] + 1, coord[1])
        below2 = (coord[0] + 2, coord[1])
        below3 = (coord[0] + 3, coord[1])
        is_in_place = coord[1] == rooms_col[c] \
                      and (below1 not in world or world[below1] == rooms_col[c]) \
                      and (below2 not in world or world[below2] == rooms_col[c]) \
                      and (below3 not in world or world[below3] == rooms_col[c])
        if is_in_place:
            continue
        is_blocked_in_room = coord[0] > 1\
                    and (world[coord[0] - 1, coord[1]] != '.' or (world[1, coord[1] - 1] != '.'
                                                                  and world[1, coord[1] + 1] != '.'))
        if is_blocked_in_room:
            continue
        for next_world in next_worlds_after_move(world, coord):
            next_worlds.append(next_world)

    return next_worlds


def solve(world):
    hq = [HeapWorld(0, world)]
    seen = set()
    solution_found = None
    while len(hq):
        heap_world = heapq.heappop(hq)
        energy, world = heap_world.energy, heap_world.world

        image = draw(world)
        if image in seen:
            continue
        seen.add(draw(world))

        if solution_found is not None and energy >= solution_found:
            # can no longer find better
            return solution_found

        next_worlds = get_next_worlds(world)
        for (additional_energy, w) in next_worlds:
            next_energy = energy + additional_energy
            if is_final(w):
                if solution_found is None or solution_found > next_energy:
                    solution_found = next_energy
                    continue
            heapq.heappush(hq, HeapWorld(next_energy, w))
    return world


def parse(input_path, deeper=False):
    with open(input_path, 'r') as f:
        world = {}
        lines = f.readlines()
        if deeper:
            lines = lines[:3] + ['  #D#C#B#A#  ', '  #D#B#A#C#  '] + lines[3:]
        for (i, line) in enumerate(lines):
            for (j, c) in enumerate(line):
                if c in 'ABCD.':
                    world[i, j] = c
        return world


if __name__ == "__main__":
    input_file = "data.txt"
    parsed = parse(input_file)
    print('Part 1 :', solve(parsed))
    parsed2 = parse(input_file, True)
    print('Part 2 :', solve(parsed2))
