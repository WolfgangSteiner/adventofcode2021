import numpy as np
import heapq
from collections import defaultdict


def parse_matrix(filename):
    lines = [line.rstrip() for line in open(filename).readlines()]
    return np.array([[int(x) for x in line] for line in lines])


def manhatten_distance(pos_a, pos_b):
    return np.sum(abs(np.array(pos_b) - np.array(pos_a)))


def get_neighbors(pos, matrix_shape):
    rows, cols = matrix_shape
    result = []
    for row in range(max(pos[0]- 1, 0), min(pos[0] + 2, rows)):
        result.append((row, pos[1]))
    for col in range(max(pos[1] - 1, 0), min(pos[1] + 2, cols)):
        result.append((pos[0], col))

    return result


def calculate_risk(matrix, came_from, start_pos, end_pos):
    result = 0
    current_pos = end_pos
    while (current_pos != start_pos):
        result += get_weight(matrix, current_pos)
        current_pos = came_from[current_pos]
    return result


def get_weight(matrix, pos):
    rows, cols = matrix.shape
    row, col = pos
    weight = matrix[pos[0] % rows, pos[1] % cols]
    tile_pos = [row // rows, col // cols]
    weight_offset = np.sum(tile_pos)
    return ((weight + weight_offset) - 1) % 9 + 1


def a_star(matrix, start_pos, end_pos, factor):
    int_max = np.iinfo(int).max
    g_score = defaultdict(lambda:int_max)
    f_score = defaultdict(lambda:int_max)
    g_score[start_pos] = 0
    f_score[end_pos] = manhatten_distance(start_pos, end_pos)
    came_from = {}
    open_set = []
    heapq.heappush(open_set, (f_score[start_pos], start_pos))
    rows, cols = matrix.shape
    matrix_shape = [rows * factor, cols * factor]

    while len(open_set):
        current_f_score, current = heapq.heappop(open_set)
        if current == end_pos:
            return calculate_risk(matrix, came_from, start_pos, end_pos)

        for neighbor in get_neighbors(current, matrix_shape):
            weight = get_weight(matrix, neighbor)
            tentative_g_score = g_score[current] + weight
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                neighbor_f_score = tentative_g_score + manhatten_distance(neighbor, end_pos)
                f_score[neighbor] = neighbor_f_score
                if neighbor not in open_set:
                    heapq.heappush(open_set, (neighbor_f_score, neighbor))


def main():
    matrix = parse_matrix("data/day15.txt")
    start_pos = (0,0)
    rows, cols = matrix.shape
    end_pos = (rows - 1, cols - 1)
    res1 = a_star(matrix, start_pos, end_pos, factor=1)
    print(f"Part One: {res1}")
    factor = 5
    end_pos = (rows * factor - 1, cols * factor - 1)
    res2 = a_star(matrix, start_pos, end_pos, factor=5)
    print(f"Part Two: {res2}")


if __name__ == "__main__":
    main()
