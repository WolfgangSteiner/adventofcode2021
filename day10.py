import numpy as np

matching_symbols = {'(':')', '{':'}', '[':']', '<':'>'}

def parse_input(filename):
    result = []
    with open(filename) as f:
       return [l.rstrip() for l in f.readlines()]

def check_line(line):
    matching_symbols = {'(':')', '{':'}', '[':']', '<':'>'}
    score = {')':3, ']':57, '}':1197, '>':25137}
    stack = []
    for c in line:
        if c in "([{<":
            stack.insert(0, c)
        elif len(stack) == 0:
            return score[c]
        else:
            front = stack.pop(0)
            if matching_symbols[front] != c:
                return score[c]
    return 0


def calculate_score(stack):
    score = {')':1, ']':2, '}':3, '>':4}
    completion = [matching_symbols[c] for c in stack]
    res = 0
    for c in completion:
        res = res * 5 + score[c]
    return res


def complete_line(line):
    stack = []
    for c in line:
        if c in "([{<":
            stack.insert(0, c)
        else:
            assert(len(stack)>0)
            front = stack.pop(0)
            assert(matching_symbols[front] == c)
    return calculate_score(stack)

def part_one(filename):
    input = parse_input(filename)
    return sum([check_line(l) for l in input])


def part_two(filename):
    input = parse_input(filename)
    incomplete_lines = [l for l in input if check_line(l) == 0]
    return int(np.median([complete_line(l) for l in incomplete_lines]))


def main():
    res1 = part_one("data/day10.txt")
    print(f"Part One: {res1}")
    res2 = part_two("data/day10.txt")
    print(f"Part Two: {res2}")

if __name__ == "__main__":
    main()
