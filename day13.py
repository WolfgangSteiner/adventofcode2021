import numpy as np

def parse_input(filename):
    file = open(filename)
    input = [line.rstrip() for line in file.readlines()]
    coords = [line.split(',') for line in input if "," in line]
    coords = np.array([[int(x), int(y)] for x,y in coords])
    folds = [line.split()[-1].split("=") for line in input if line.startswith("fold")]
    folds = [[coord, int(value)] for coord, value in folds]
    return coords, folds


def print_sheet(sheet):
    for row in sheet:
        print("".join(['.' if x == 0 else '#' for x in row]))
    print()


def fold_sheet_y(sheet, position):
    rows, cols = sheet.shape
    new_sheet = sheet[0:position,:]
    rows_lower_part = rows - position - 1
    end_row = position - 1
    start_row = position - rows_lower_part
    new_sheet += np.flip(sheet[position+1:,:], axis=0)
    return new_sheet


def fold_sheet(sheet, fold):
    direction, position = fold
    if direction == 'x':
        new_sheet = fold_sheet_y(sheet.T, position).T
    else:
        new_sheet = fold_sheet_y(sheet, position)
    return new_sheet
    

def count_sheet(sheet):
    return np.sum(sheet > 0)


def prepare_data(filename):
    coords, folds = parse_input(filename)
    cols, rows = np.max(coords + 1, axis=0)
    sheet = np.zeros((rows, cols), dtype=int)
    for x, y in coords:
        sheet[y, x] = 1
    return sheet, folds


def part_one(filename):
    sheet, folds = prepare_data(filename)
    sheet = fold_sheet(sheet, folds[0])
    return count_sheet(sheet)


def part_two(filename):
    sheet, folds = prepare_data(filename)
    for fold in folds:
        sheet = fold_sheet(sheet, fold)
    print_sheet(sheet)


def main():
    res1 = part_one("data/day13.txt")
    print(f"Part One: {res1}")
    print(f"Part Two")
    part_two("data/day13.txt")

if __name__ == "__main__":
    main()
