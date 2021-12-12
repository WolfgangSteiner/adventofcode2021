import numpy as np
from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Path:
    sequence: list
    visited: list
    has_extra_visit: bool = True



class Graph:
    nodes_to_id: dict
    id_to_nodes: dict
    adjacency_matrix: np.array
    num_nodes: int
    start_node_id: int
    end_node_id: int
    allow_extra_visit: bool

    def __init__(self, nodes_to_id, id_to_nodes, adjacency_matrix):
        self.nodes_to_id = nodes_to_id
        self.id_to_nodes = id_to_nodes
        self.adjacency_matrix = adjacency_matrix
        self.start_node_id = nodes_to_id["start"]
        self.end_node_id = nodes_to_id["end"]
        self.num_nodes = len(nodes_to_id)
        self.allow_extra_visit = False

    def get_adjacent_nodes(self, node_id):
        return np.where(self.adjacency_matrix[node_id] == 1)[0]

    def extend_path(self, path, node_id):
        new_path = deepcopy(path)
        new_path.sequence.append(node_id)
        if self.is_small_node(node_id):
            new_path.visited[node_id] = 1

        return new_path

    def is_small_node(self, node_id):
        node_name = self.id_to_nodes[node_id]
        return node_name[0].islower()

    def is_path_complete(self, path):
        return path.sequence[0] == self.start_node_id and path.sequence[-1] == self.end_node_id

    def is_path_dead_end(self, path):
        last_node = path.sequence[-1]
        adjacent_nodes = self.get_adjacent_nodes(last_node)
        return np.all(path.visited[adjacent_nodes] == 1) and not path.has_extra_visit

    def find_paths(self):
        visited = np.zeros(self.num_nodes)
        visited[self.start_node_id] = 1
        paths = [Path([self.start_node_id], visited)]
        complete_paths = []
        while len(paths):
            path = paths.pop(0)
            last_node_in_path = path.sequence[-1]
            adjacent_nodes = self.get_adjacent_nodes(last_node_in_path)
            for next_node in adjacent_nodes:
                new_path = self.extend_path(path, next_node)
                if path.visited[next_node] == 1:
                    if self.allow_extra_visit and path.has_extra_visit and next_node != self.start_node_id:
                        new_path.has_extra_visit = False
                    else:
                        continue
                if self.is_path_complete(new_path):
                    complete_paths.append(new_path)
                elif self.is_path_dead_end(new_path):
                    pass
                else:
                    paths.insert(0, new_path)
        return complete_paths

    def print_path(self, path):
        print(",".join([self.id_to_nodes[node] for node in path.sequence]))


def parse_input(filename):
    node_id = 0
    nodes_to_id = {}
    id_to_nodes = {}
    vertices = []
    for line in open(filename).readlines():
        node_a, node_b = line.rstrip().split("-")
        if node_a not in nodes_to_id:
            nodes_to_id[node_a] = node_id
            id_to_nodes[node_id] = node_a
            node_id += 1

        if node_b not in nodes_to_id:
            nodes_to_id[node_b] = node_id
            id_to_nodes[node_id] = node_b
            node_id += 1

        vertices.append((nodes_to_id[node_a], nodes_to_id[node_b]))

    num_nodes = node_id
    adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
    for vertex in vertices:
        adjacency_matrix[vertex] = 1
    adjacency_matrix += adjacency_matrix.T

    return Graph(nodes_to_id, id_to_nodes, adjacency_matrix)


def part_one(filename):
    graph = parse_input(filename)
    return len(graph.find_paths())


def part_two(filename):
    graph = parse_input(filename)
    graph.allow_extra_visit = True
    paths = graph.find_paths()
    return len(paths)


def test_part_one():
    assert(part_one("data/day12_test1.txt") == 10)
    assert(part_one("data/day12_test2.txt") == 19)
    assert(part_one("data/day12_test3.txt") == 226)


def test_part_two():
    assert(part_two("data/day12_test1.txt") == 36)
    assert(part_two("data/day12_test2.txt") == 103)
    assert(part_two("data/day12_test3.txt") == 3509)


def main():
    test_part_one()
    res1 = part_one("data/day12.txt")
    print(f"Part One: {res1}")
    test_part_two()
    res2 = part_two("data/day12.txt")
    print(f"Part Two: {res2}")


if __name__ == "__main__":
    main()

