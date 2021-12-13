import numpy as np


def parse_input(filename):
    file = open(filename)
    input = [line.rstrip() for line in file.readlines()]
    coords = [line.split(',') for line in input if "," in line]
    coords = {(int(x), int(y)) for x, y in coords}
    folds = [line.split()[-1].split("=") for line in input if line.startswith("fold")]
    folds = [[coord, int(value)] for coord, value in folds]
    return coords, folds


def find_max(coords):
    max_x = -9999999
    max_y = -9999999
    for x, y in coords:
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    return max_x, max_y


def find_min(coords):
    min_x = 9999999
    min_y = 9999999
    for x, y in coords:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
    return min_x, min_y


def normalize_coords(coords):
    min_x, min_y = find_min(coords)
    return {(x - min_x, y - min_y) for x, y in coords}


def print_coords(coords):
    coords = normalize_coords(coords)
    max_x, max_y = find_max(coords)
    sheet = np.zeros((max_y + 1, max_x + 1))
    for x, y in coords:
        sheet[y, x] = 1
    print_sheet(sheet)


def print_sheet(sheet):
    for row in sheet:
        print("".join([' ' if x == 0 else '#' for x in row]))
    print()


def fold_sheet(coords, fold):
    direction, position = fold
    if direction == 'x':
        folded = {(x if x < position else 2 * position - x, y) for x, y in coords}
    else:
        folded = {(x, y if y < position else 2 * position - y) for x, y in coords}
    return normalize_coords(folded) 


def part_one(filename):
    coords, folds = parse_input(filename)
    coords = fold_sheet(coords, folds[0])
    return len(coords) 


def part_two(filename):
    coords, folds = parse_input(filename)
    for fold in folds:
        coords = fold_sheet(coords, fold)
    print_coords(coords)


def main():
    res1 = part_one("data/day13_test.txt")
    print(f"Part One: {res1}")
    print()
    print(f"Part Two:")
    part_two("data/day13.txt")


if __name__ == "__main__":
    main()
