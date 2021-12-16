import numpy as np

TYPE_LITERAL = 4
TYPE_SUM = 0
TYPE_PRODUCT = 1
TYPE_MINIMUM = 2
TYPE_MAXIMUM = 3
TYPE_GREATER_THAN = 5
TYPE_LESS_THAN = 6
TYPE_EQUAL_TO = 7

hex_map = {
    '0': [0,0,0,0],
    '1': [0,0,0,1],
    '2': [0,0,1,0],
    '3': [0,0,1,1],
    '4': [0,1,0,0],
    '5': [0,1,0,1],
    '6': [0,1,1,0],
    '7': [0,1,1,1],
    '8': [1,0,0,0],
    '9': [1,0,0,1],
    'A': [1,0,1,0],
    'B': [1,0,1,1],
    'C': [1,1,0,0],
    'D': [1,1,0,1],
    'E': [1,1,1,0],
    'F': [1,1,1,1]
}


def bits_to_value(bits):
    result = 0
    shift = len(bits) - 1
    for bit in bits:
        result = result | (bit << shift)
        shift -= 1
    assert(shift == -1)
    return result


class Packet:
    def __init__(self, hex_literals, bit_buffer=None):
        self.version = 0
        self.type = 0
        self.num_bits = 0
        self.num_bits_of_packets = -1
        self.num_packets = -1
        self.value = 0
        self.sub_packets = []
        self.bit_buffer = bit_buffer.copy() if bit_buffer is not None else []
        self.parse_hex(hex_literals)

    def get_bits(self, num_bits, hex_literals):
        self.num_bits += num_bits
        while len(self.bit_buffer) < num_bits:
            self.bit_buffer += hex_map[hex_literals.pop(0)]
        result = self.bit_buffer[0:num_bits]
        self.bit_buffer = self.bit_buffer[num_bits:]
        return result

    def get_value(self, num_bits, hex_literals):
        bits = self.get_bits(num_bits, hex_literals)
        return bits_to_value(bits)

    def calc_bits_of_sub_packets(self):
        result = 0
        for p in self.sub_packets:
            result += p.num_bits
            result += p.calc_bits_of_sub_packets()
        return result

    def parse_sub_package(self, hex_literals):
        new_packet = Packet(hex_literals, self.bit_buffer)
        self.sub_packets.append(new_packet)
        self.bit_buffer = new_packet.bit_buffer
        new_packet.bit_buffer = []

    def parse_hex(self, hex_literals):
        self.version = self.get_value(3, hex_literals)
        self.type = self.get_value(3, hex_literals)
        if self.type == TYPE_LITERAL:
            last_group = False
            bits_for_literal = []
            while not last_group:
                bits = self.get_bits(5, hex_literals)
                last_group = (bits[0] == 0)
                bits_for_literal += bits[1:]
            self.value = bits_to_value(bits_for_literal)
        else:
            length_type_id = self.get_value(1, hex_literals)
            self.sub_packets = []
            if length_type_id == 0:
                self.num_bits_of_packets = self.get_value(15, hex_literals)
                while self.calc_bits_of_sub_packets() < self.num_bits_of_packets:
                    self.parse_sub_package(hex_literals)
            else:
                self.num_packets = self.get_value(11, hex_literals)
                for i in range(self.num_packets):
                    self.parse_sub_package(hex_literals)

    def get_all_version_numbers(self):
        result = [self.version]
        for p in self.sub_packets:
            result += p.get_all_version_numbers()
        return result

    def evaluate_expression(self):
        if self.type == TYPE_LITERAL:
            return self.value
        else:
            values = [p.evaluate_expression() for p in self.sub_packets]
            if self.type == TYPE_SUM:
                return np.sum(values)
            elif self.type == TYPE_PRODUCT:
                return np.prod(values)
            elif self.type == TYPE_MINIMUM:
                return np.min(values)
            elif self.type == TYPE_MAXIMUM:
                return np.max(values)
            elif self.type == TYPE_GREATER_THAN:
                assert(len(values) == 2)
                return int(values[0] > values[1])
            elif self.type == TYPE_LESS_THAN:
                assert(len(values) == 2)
                return int(values[0] < values[1])
            elif self.type == TYPE_EQUAL_TO:
                assert(len(values) == 2)
                return int(values[0] == values[1])
            else:
                print("Unknown operator type")
                assert(False)
                return 0


def part_one(hex_string):
    packet = Packet(list(hex_string))
    version_numbers = packet.get_all_version_numbers()
    return np.sum(version_numbers)


def part_two(hex_string):
    packet = Packet(list(hex_string))
    return packet.evaluate_expression()


def run_tests():
    assert(bits_to_value([1,1,1]) == 7)

    input_1 = "D2FE28"
    p1 = Packet(list(input_1))
    assert(p1.type == TYPE_LITERAL)
    assert(p1.version == 6)
    assert(p1.value == 2021)

    input_2 = "38006F45291200"
    p2 = Packet(list(input_2))
    assert(p2.version == 1)
    assert(p2.type == 6)
    assert(p2.num_bits_of_packets == 27)

    input_3 = "EE00D40C823060"
    p3 = Packet(list(input_3))
    assert(p3.version == 7)
    assert(p3.type == 3)
    assert(p3.num_packets == 3)

    assert(part_one("8A004A801A8002F478") == 16)
    assert(part_one("620080001611562C8802118E34") == 12)
    assert(part_one("C0015000016115A2E0802F182340") == 23)
    assert(part_one("A0016C880162017C3686B18A3D4780") == 31)

    assert(part_two("C200B40A82") == 3)
    assert(part_two("04005AC33890") == 54)
    assert(part_two("880086C3E88112") == 7)
    assert(part_two("CE00C43D881120") == 9)
    assert(part_two("D8005AC2A8F0") == 1)
    assert(part_two("F600BC2D8F") == 0)
    assert(part_two("9C005AC2F8F0") == 0)
    assert(part_two("9C0141080250320F1802104A08") == 1)


def main():
    run_tests()
    input = open("data/day16.txt").read().rstrip()
    print("Part One:", part_one(input))
    print("Part Two:", part_two(input))


if __name__ == "__main__":
    main()