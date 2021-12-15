import numpy as np
from collections import defaultdict

def parse_matrix(filename):
    lines = [line.rstrip() for line in open(filename).readlines()]
    return np.array([[int(x) for x in line] for line in lines])


def manhatten_distance(pos_a, pos_b):
    return np.sum(abs(np.array(pos_b) - np.array(pos_a)))


def get_neighbors(pos, matrix):
    rows, cols = matrix.shape
    result = []
    for row in range(max(pos[0] - 1, 0), min(pos[0] + 2, rows)):
        result.append((row, pos[1]))
    for col in range(max(pos[1] - 1, 0), min(pos[1] + 2, cols)):
        result.append((pos[0], col))

    return result


def calculate_risk(matrix, came_from, start_pos, end_pos):
    result = 0
    current_pos = end_pos
    while (current_pos != start_pos):
        result += matrix[current_pos]
        current_pos = came_from[current_pos]
    return result


def a_star(matrix, start_pos, end_pos):
    int_max = np.iinfo(int).max
    g_score = defaultdict(lambda:int_max)
    f_score = defaultdict(lambda:int_max)
    g_score[start_pos] = 0
    f_score[end_pos] = manhatten_distance(start_pos, end_pos)
    came_from = {}
    open_set = [start_pos]

    while len(open_set):
        open_set.sort(key=lambda pos: f_score[pos])
        current = open_set.pop(0)
        if current == end_pos:
            return calculate_risk(matrix, came_from, start_pos, end_pos)

        for neighbor in get_neighbors(current, matrix):
            weight = matrix[neighbor]
            tentative_g_score = g_score[current] + weight
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhatten_distance(neighbor, end_pos)
                if neighbor not in open_set:
                    open_set.append(neighbor)


def main():
    matrix = parse_matrix("data/day15.txt")
    start_pos = (0,0)
    end_pos = (matrix.shape[0] - 1, matrix.shape[1] - 1)
    res1 = a_star(matrix, start_pos, end_pos)
    print(f"Part One: {res1}")


if __name__ == "__main__":
    main()
