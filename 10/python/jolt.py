#!/usr/bin/env python3

import argparse
from typing import Dict, List, TextIO, Tuple
import sys

Graph = Dict[int, List[int]]


def get_diffs(adapters: List[int]) -> Tuple[int, int]:
    """
    Return the number of 1 and 3 jolt differences for a list of adapters.
    """
    sorted_adapters = sorted(adapters)
    curr_jolt = 0
    diff_one = 0
    diff_three = 1
    for a in sorted_adapters:
        diff = a - curr_jolt
        if diff == 1:
            diff_one += 1
        elif diff == 3:
            diff_three += 1
        else:
            raise Exception(f"Adapter {a} cannot be connected")
        curr_jolt = a
    return diff_one, diff_three


def build_graph(adapters: List[int]) -> Graph:
    nodes = [0]
    nodes.extend(sorted(adapters))
    graph: Graph = {}
    for i, node in enumerate(nodes):
        graph[node] = []
        for j in range(i+1, i+4):
            if j >= len(nodes):
                break
            if nodes[j] - node > 3:
                break
            graph[node].append(nodes[j])
    return graph


def dfs(graph: Graph, completed: Dict[int, int], start: int) -> int:
    if start not in graph:
        raise ValueError(f"Node {start} is not in graph.")
    neighbours = graph[start]
    if not neighbours:
        # Found the leaf node
        return 1
    summa = 0
    for n in neighbours:
        # process node
        if n in completed:
            summa += completed[n]
        else:
            summa += dfs(graph, completed, n)
    completed[start] = summa
    return summa


def find_all_paths(data: List[int]) -> int:
    g = build_graph(data)
    completed: Dict[int, int] = {}
    return dfs(g, completed, 0)


def read_input(in_stream: TextIO) -> List[int]:
    result = []
    for line in in_stream:
        result.append(int(line.strip()))
    return result


def main() -> None:
    aparser = argparse.ArgumentParser()
    aparser.add_argument("problem", choices=["one", "two"])
    args = aparser.parse_args()
    data = read_input(sys.stdin)
    if args.problem == "one":
        diff_one, diff_three = get_diffs(data)
        print(diff_one * diff_three)
    else:
        print(find_all_paths(data))


if __name__ == "__main__":
    main()
