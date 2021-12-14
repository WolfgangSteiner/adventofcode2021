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


def polymerize_pair(pair, rules, num_steps, elements_count):
    if pair in rules:
        new_element = rules[pair]
        elements_count[new_element] += 1
        if num_steps > 1:
            polymerize_pair(pair[0] + new_element, rules, num_steps - 1, elements_count)
            polymerize_pair(new_element + pair[1], rules, num_steps - 1, elements_count)


def count_elements_of_polymerization(polymer, rules, num_steps):
    elements_count = count_elements(polymer)
    for i in range(len(polymer) - 1):
        pair = polymer[i:i+2]
        polymerize_pair(pair, rules, num_steps, elements_count)
    return elements_count


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
        polymer = polymerize_once(polymer, rules)
    return polymer


def count_elements(polymer):
    elements = defaultdict(int)    
    for element in polymer:
        elements[element] += 1
    return elements


def build_graph(rules):
    nodes = set()
    for pair, element in rules.items():
        nodes.add(pair)
        nodes.add(pair[0] + element)
        nodes.add(element + pair[1])
    
    num_nodes = len(nodes)
    nodes = list(nodes)
    nodes_to_index = { pair: index for index, pair in enumerate(nodes) }

    adjacency_matrix = np.zeros((num_nodes, num_nodes), np.int64)
    
    for pair, element in rules.items():
        pair_a = pair[0] + element
        pair_b = element + pair[1]
        idx = nodes_to_index[pair]
        idx_a = nodes_to_index[pair_a]
        idx_b = nodes_to_index[pair_b]
        adjacency_matrix[idx, idx_a] = 1
        adjacency_matrix[idx, idx_b] = 1

    return adjacency_matrix, nodes, nodes_to_index


def test_part_one(filename):
    polymer, rules = parse_input(filename)
    p1 = polymerize_once(polymer, rules)
    assert(p1 == "NCNBCHB")
    p2 = polymerize_once(p1, rules)
    assert(p2 == "NBCCNBBBCBHCB")
    p3 = polymerize_once(p2, rules)
    assert(p3 == "NBBBCNCCNBBNBNBBCHBHHBCHB")
    p4 = polymerize_once(p3, rules)
    assert(p4 == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB")
    print(count_elements(p4))
    print(count_elements_of_polymerization(polymer, rules, 4))


def perform_polymerization(filename, num_steps):
    template, rules = parse_input(filename)
    polymer = polymerize(template, rules, num_steps)
    elements = count_elements(polymer)
    min_value = min(elements.values())
    max_value = max(elements.values())
    return max_value - min_value 


def part_one(filename):
    return perform_polymerization(filename, 10)


def compute_result_for_pair(pair, prod, nodes, nodes_to_id, results):
    start_node_id = nodes_to_id[pair]
    results[pair[0]] += 1
    for node, node_id in nodes_to_id.items():
        num = prod[start_node_id, node_id]
        #results[node[0]] += num
        results[node[1]] += num
       

def compute_result(polymer, prod, nodes, nodes_to_id):
    results = defaultdict(int)
    for i in range(len(polymer) - 1):
        pair = polymer[i:i+2]
        compute_result_for_pair(pair, prod, nodes, nodes_to_id, results)
    results[polymer[-1]] += 1
    return results


def test_part_two(filename):
    polymer, rules = parse_input(filename)
    adj, nodes, nodes_to_id = build_graph(rules)
    num_steps = 10
    prod = np.linalg.matrix_power(adj, num_steps)
    results = compute_result(polymer, prod, nodes, nodes_to_id)
    print(prod)
    print(results)
    print(compute_score(results))


def compute_score(results):
    min_value = min(results.values())
    max_value = max(results.values())
    return max_value - min_value 


def part_two(filename):
    polymer, rules = parse_input(filename)
    adj, nodes, nodes_to_id = build_graph(rules)
    prod = np.linalg.matrix_power(adj, 40)
    results = compute_result(polymer, prod, nodes, nodes_to_id)
    return(compute_score(results))


def main():
    test_part_one("data/day14_test.txt")
    res1 = part_one("data/day14.txt")
    print(f"Part One: {res1}")
    print()
    res2 = part_two("data/day14.txt")
    print(f"Part Two: {res2}")


if __name__ == "__main__":
    main()
