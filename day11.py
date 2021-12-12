import numpy as np


def parse_input(filename):
    with open(filename) as file:
        data = [line.rstrip() for line in file.readlines()]
        return np.array(
            [[int(x) for x in row] for row in data],
            dtype=np.uint8)


def print_grid(grid):
    for row in range(grid.shape[0]):
        print("".join([str(x) for x in grid[row]]))


def neighbors(pos, grid):
    rows, cols = grid.shape
    res = []
    for y in np.arange(max(0, pos[0] - 1), min(pos[0] + 2, rows)):
        for x in np.arange(max(0, pos[1] - 1), min(pos[1] + 2, cols)):
            res.append((y, x))
    return res


def iterate_grid(grid):
    rows, cols = grid.shape
    res = []
    for y in np.arange(0, rows):
        for x in np.arange(0, cols):
            res.append((y, x))
    return res


def simulate_step(grid):
    grid += 1
    flashes = 0

    while np.any(grid == 10):
        new_grid = grid.copy()
        flashes += np.sum(grid == 10)
        for pos in iterate_grid(new_grid):
            val = grid[pos]
            if val == 10:
                for npos in neighbors(pos, grid):
                    if new_grid[npos] != 255:
                        new_grid[npos] = min(10, new_grid[npos] + 1)
        new_grid[grid == 10] = 255
        grid = new_grid

    grid[grid == 255] = 0
    return grid, flashes


def part_one(filename, num_steps):
    grid = parse_input(filename)
    flashes = 0
    for i in range(num_steps):
        grid, flash_count = simulate_step(grid)
        flashes += flash_count
    return flashes


def part_two(filename):
    grid = parse_input(filename)
    step = 1
    while True:
        grid, flash_count = simulate_step(grid)
        if np.all(grid == 0):
            break
        step += 1
    return step


def main():
    assert(part_one("data/day11_test.txt", 100) == 1656)
    res1 = part_one("data/day11.txt", 100)
    print(f"Part One: {res1}")
    assert(part_two("data/day11_test.txt") == 195)
    res2 = part_two("data/day11.txt")
    print(f"Part Two: {res2}")


if __name__ == "__main__":
    main()
