import numpy as np
from collections import defaultdict

def parse_input(filename):
    file = open(filename)
    input = [line.rstrip() for line in file.readlines()]
    template = input[0]
    rules = dict()

    for line in input[2:]:
        pair, insert = line.split(" -> ")
        rules[pair] = insert

    return template, rules


def polymerize_once(polymer, rules):
    result = ""
    for i in range(len(polymer) - 1):
        pair = polymer[i:i + 2]
        result += pair[0]
        if pair in rules:
            result += rules[pair]

    result += polymer[-1]
    return result


def polymerize(polymer, rules, num_steps):
    for i in range(num_steps):
        print(f"{i}/{num_steps}")
        polymer = polymerize_once(polymer, rules)
    return polymer


def count_elements(polymer):
    elements = defaultdict(int)    
    for element in polymer:
        elements[element] += 1
    return elements


def test_part_one(filename):
    polymer, rules = parse_input(filename)
    polymer = polymerize_once(polymer, rules)
    assert(polymer == "NCNBCHB")
    polymer = polymerize_once(polymer, rules)
    assert(polymer == "NBCCNBBBCBHCB")
    polymer = polymerize_once(polymer, rules)
    assert(polymer == "NBBBCNCCNBBNBNBBCHBHHBCHB")
    polymer = polymerize_once(polymer, rules)
    assert(polymer == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB")
    print(count_elements(polymer))


def perform_polymerization(filename, num_steps):
    template, rules = parse_input(filename)
    polymer = polymerize(template, rules, num_steps)
    elements = count_elements(polymer)
    min_value = min(elements.values())
    max_value = max(elements.values())
    return max_value - min_value 


def part_one(filename):
    return perform_polymerization(filename, 10)


def part_two(filename):
    return perform_polymerization(filename, 40)


def main():
    test_part_one("data/day14_test.txt")
    res1 = part_one("data/day14.txt")
    print(f"Part One: {res1}")
    print()
    res2 = part_two("data/day14_test.txt")
    print(f"Part Two: {res2}")


if __name__ == "__main__":
    main()
