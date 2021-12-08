import numpy as np
import sys

test_input = np.array((16,1,2,0,4,2,7,1,2,14), dtype=np.int32)

with open("data/day07.txt") as f:
    input = np.array([int(x) for x in f.read().split(",")], dtype=np.int32)

def calc_fuel_part1(input, target_val):
    return np.sum(np.abs(input - np.ones_like(input) * np.median(input)))

def calc_fuel_part2(input, target_val):
    abs_diff = np.abs(input - np.ones_like(input) * target_val);
    return np.sum(0.5 * abs_diff * (abs_diff + 1))

def calc_solution2(input):
    target_val = np.round(np.mean(input))
    result = sys.float_info.max

    for delta in range(-1,1):
        cur_val = target_val + delta
        fuel = calc_fuel_part2(input, cur_val)
        if (fuel < result):
            result = fuel

    return result

def main():
    print("Part 1: ", calc_fuel_part1(input, np.median(input)))

    res2 = calc_solution2(input)
    print(f"Part 2: {res2}");


if __name__ == "__main__":
    main()
