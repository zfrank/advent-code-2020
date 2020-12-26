#!/usr/bin/env python3

import argparse
from collections import defaultdict
import re
from typing import Dict, List, TextIO, Set, Tuple
import sys

Graph = Dict[str, List[Tuple[int, str]]]

REGEX_NEIGH = r"(\d+) (\w+ \w+) bag"


def parse_line(line: str) -> Tuple[str, List[Tuple[int, str]]]:
    """
    Parses one line of text with bag information. Examples:
      "light red bags contain 1 bright white bag, 2 muted yellow bags."
      "faded blue bags contain no other bags."
    Returns the first bad identifier and a list with tuples, each containing
    the number of contained bags and their identifieds.
    For the examples above, this function would respectively return:
      "light red", [(1, "bright white"), (2, "muted yellow")]
      "faded blue", []
    """
    node, neigh_raw = line.split(" bags contain ")
    if neigh_raw == "no other bags.":
        return node, []
    matches = re.findall(REGEX_NEIGH, neigh_raw)
    parsed_matches = [(int(x), y) for x, y in matches]
    return node, parsed_matches


def build_graphs(in_stream: TextIO) -> Tuple[Graph, Graph]:
    graph = defaultdict(list)
    revgraph = defaultdict(list)
    for line in in_stream:
        line = line.strip()
        node, neighs = parse_line(line)
        graph[node] = neighs
        for ne in neighs:
            revgraph[ne[1]].append((ne[0], node))
    return graph, revgraph


def bfs(graph: Graph, start: str) -> Set[str]:
    visited = set()
    pending = [start]
    while pending:
        new_pending = []
        for n in pending:
            for nn in graph[n]:
                nn_name = nn[1]
                if nn_name not in visited:
                    new_pending.append(nn_name)
            visited.add(n)
        pending = new_pending
    return visited


def count_bags(graph: Graph, start: str) -> int:
    total = 0
    neighs = graph[start]
    if not neighs:
        return 0
    for neigh in neighs:
        total += neigh[0] + (neigh[0] * count_bags(graph, neigh[1]))
    return total


def main() -> None:
    aparser = argparse.ArgumentParser()
    aparser.add_argument("problem", choices=["one", "two"])
    args = aparser.parse_args()
    graph, revgraph = build_graphs(sys.stdin)
    if args.problem == "one":
        print(len(bfs(revgraph, "shiny gold")) - 1)
    else:
        print(count_bags(graph, "shiny gold"))


if __name__ == "__main__":
    main()
