import math


class Packet:
    def __init__(self, v, type, bits, number=None, packets=None):
        self.version = v
        self.type = type
        self.number = number
        self.bits = bits
        self.packets = packets if packets is not None else []
    

def read_packet(binary):
    ptr = 0
    v = int(binary[ptr:ptr+3], 2)
    ptr += 3
    type = int(binary[ptr:ptr+3], 2)
    ptr += 3
    if type == 4:  # literal value
        last_block = False
        number = ''
        while not last_block:
            last_block = int(binary[ptr]) != 1
            ptr += 1
            number += binary[ptr:ptr+4]
            ptr += 4
        number = int(number, 2)
        return Packet(v, type, ptr, number)
    else:  # operator
        length_type_id = int(binary[ptr])
        ptr += 1
        packets = []
        if length_type_id == 0:  # 15 bits length of subpackets
            length = int(binary[ptr:ptr+15], 2)
            ptr += 15
            end = ptr + length
            while ptr < end:
                packet = read_packet(binary[ptr:])
                ptr += packet.bits
                packets.append(packet)
            return Packet(v, type, ptr, None, packets)

        else:   # 11 bits number of subpackets
            subpackets_nb = int(binary[ptr:ptr+11], 2)
            ptr += 11
            for i in range(subpackets_nb):
                packet = read_packet(binary[ptr:])
                ptr += packet.bits
                packets.append(packet)
            return Packet(v, type, ptr, None, packets)


def sum_version(packet):
    return packet.version + sum([sum_version(p) for p in packet.packets])


def solve_part1(binary):
    return sum_version(read_packet(binary))


def calculate(packet):
    if packet.type == 0:
        return sum([calculate(p) for p in packet.packets])
    elif packet.type == 1:
        return math.prod([calculate(p) for p in packet.packets])
    elif packet.type == 2:
        return min([calculate(p) for p in packet.packets])
    elif packet.type == 3:
        return max([calculate(p) for p in packet.packets])
    elif packet.type == 4:
        return packet.number
    elif packet.type == 5:
        return 1 if calculate(packet.packets[0]) > calculate(packet.packets[1]) else 0 
    elif packet.type == 6:
        return 1 if calculate(packet.packets[0]) < calculate(packet.packets[1]) else 0 
    elif packet.type == 7:
        return 1 if calculate(packet.packets[0]) == calculate(packet.packets[1]) else 0 


def solve_part2(binary):
    return calculate(read_packet(binary))


def parse(input_path):
    with open(input_path, 'r') as f:
        row = f.readline().strip()
        return bin(int(row, 16))[2:].zfill(len(row) * 4)  # remove 0b prefix


if __name__ == "__main__":
    parsed = parse("data.txt")
    print('Part 1 :', solve_part1(parsed))
    print('Part 2 :', solve_part2(parsed))
