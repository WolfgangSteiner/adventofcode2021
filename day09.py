import numpy as np


def parse_input(filename):
    res = []
    with open(filename, "r") as f:
        for l in f.readlines():
            l = l.rstrip()
            res.append([int(x) for x in l])

    return np.array(res, dtype=np.int32)


def find_low_points_row_wise(array):
    res = np.zeros_like(array)
    rows = array.shape[0]
    cols = array.shape[1]
    int_max = np.iinfo(np.int32).max
    for row in range(rows):
        for i in range(cols):
            cur_value = array[row, i]
            prev_value = array[row, i - 1] if i > 0 else int_max
            next_value = array[row, i + 1] if i < cols - 1 else int_max
            if prev_value > cur_value < next_value :
                res[row, i] = 1
    return res


def get_low_points(array):
    rows = array.shape[0]
    cols = array.shape[1]
    res = []
    for row in range(rows):
        for col in range(cols):
            if array[row, col] == 1:
                res.append((row,col))
    return res


def find_low_points(array):
    row_wise = find_low_points_row_wise(array)
    col_wise = find_low_points_row_wise(array.T).T
    return row_wise * col_wise


def find_neighbors(pos, array, visited):
    row, col = pos
    res = []
    if row > 0:
        up = (row - 1, col)
        if array[up] < 9 and visited[up] == 0:
            res.append(up)
    if row < array.shape[0] - 1:
        down = (row + 1, col)
        if array[down] < 9 and visited[down] == 0:
            res.append(down)
    if  col > 0:
        left = (row, col - 1)
        if array[left] < 9 and visited[left] == 0:
            res.append(left)
    if col < array.shape[1] - 1:
        right = (row, col + 1)
        if array[right] < 9 and visited[right] == 0:
            res.append(right)
    
    return res


def count_basin(array, start_pos):
    visited = np.zeros_like(array)
    queue = [start_pos]
    while len(queue):
        pos = queue.pop(0)
        visited[pos] = 1
        queue += find_neighbors(pos, array, visited)
    return np.sum(visited) 


def part_one(filename):
    array = parse_input(filename)
    low_points = find_low_points(array)
    return np.sum(array * low_points + low_points)


def part_two(filename):
    array = parse_input(filename)
    low_point_matrix = find_low_points(array)
    low_points = get_low_points(low_point_matrix)
    res = 1
    basin_sizes = sorted([count_basin(array, p) for p in low_points])
    return np.prod(basin_sizes[-3:])


def main():
    res1 = part_one("data/day09.txt")
    print("Part One: ", res1)
    res2 = part_two("data/day09.txt")
    print("Part Two: ", res2)


if __name__ == "__main__":
    main()  

