class DigitClassifier:
    def __init__(self):
        self.lookup = {}
        self.reverse_lookup = {}

    def fit_top(self):
        segments_seven = self.reverse_lookup[7].split()
        segments_one = self.reverse_lookup[1].split()
        for s in segments_one:
            if s not in segments_seven:
                return s

    def segments_for_digit(self, digit):
        return self.reverse_lookup[digit].split()

    def erase_segments_for_digit(self, sym, digit):
        res = []
        segments_to_erase = self.segments_for_digit(digit)
        for s in sym.split():
            if s not in segments_to_erase:
                res.append(s)
        return res 

    def sym_contains_segments(self, sym, segments):
        for s in segments:
            if s not in sym:
                return False
        return True

    def fit_three(self):
        seven = self.reverse_lookup[7]
        for c in self.reverse_lookup[3].copy():
            if self.sym_contains_segments(c, seven):
                self.set_digit(c, 3)
                self.reverse_lookup[2].remove(c)
                self.reverse_lookup[5].remove(c)
            else:
                self.lookup[c].remove(3)

    def fit_nine(self):
        three = self.reverse_lookup[3]
        for c in self.reverse_lookup[9].copy():
            if self.sym_contains_segments(c, three):
                self.set_digit(c, 9)
                self.reverse_lookup[0].remove(c)
                self.reverse_lookup[6].remove(c)
            else:
                self.lookup[c].remove(9)

    def fit_zero_six(self):
        one = self.reverse_lookup[1]
        for c in self.reverse_lookup[0].copy():
            if self.sym_contains_segments(c, one):
                self.set_digit(c, 0)
            else:
                self.set_digit(c, 6)

    def fit_two_five(self):
        six = self.reverse_lookup[6]
        for c in self.reverse_lookup[2].copy():
            if self.sym_contains_segments(six, c):
                self.set_digit(c, 5)
            else:
                self.set_digit(c, 2)

    def fit(self, data):
        self.lookup = {}
        for digit in (0, 2, 3, 5, 6, 9):
            self.reverse_lookup[digit] = [] 

        for sym in data:
            sym = "".join(sorted(sym))
            if len(sym) == 2:
                self.set_digit(sym, 1)
            elif len(sym) == 3:
                self.set_digit(sym, 7)
            elif len(sym) == 4:
                self.set_digit(sym, 4)
            elif len(sym) == 5:
                self.set_digit(sym, [2, 3, 5])
            elif len(sym) == 6:
                self.set_digit(sym, [0, 6, 9])
            elif len(sym) == 7:
                self.set_digit(sym, 8)

        self.fit_three()
        self.fit_nine()
        self.fit_zero_six()
        self.fit_two_five()
        
    def set_digit(self, sym, value):
        self.lookup[sym] = value

        if isinstance(value, list):
            for v in value:
                self.reverse_lookup[v].append(sym)
        else:
            self.reverse_lookup[value] = sym

    def predict(self, sym):
        sym = "".join(sorted(sym))
        return self.lookup[sym]


def load_data(filename):
    res = []
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.rstrip()
            train, test = line.split(" | ")
            train = train.split()
            test = test.split()
            res.append((train, test))

    return res


def part_one(filename):
    data = load_data(filename)
    c = DigitClassifier()
    result = 0

    for (train, test) in data:
        c.fit(train)
        result += sum([1 if x in (1,4,7,8) else 0 for x in [c.predict(x) for x in test]])
    return result


def part_two(filename):
    data = load_data(filename)
    c = DigitClassifier()
    result = 0
    for (train, test) in data:
        c.fit(train)
        result += int("".join([str(c.predict(x)) for x in test]))
    return result


def test_part_one():
    assert(part_one("data/day08_test.txt") == 26)


def test_part_two():
    assert(part_two("data/day08_test.txt") == 61229)


def main():
    test_part_one()
    print("Part One: ", part_one("data/day08.txt"))
    test_part_two()
    print("Part Two: ", part_two("data/day08.txt"))


if __name__ == "__main__":
    main()
