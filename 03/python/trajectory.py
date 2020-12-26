#!/usr/bin/env python3

from typing import List, TextIO
import argparse
import sys

SLOPES = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]


def count_trees(maptext: List[str], skip_right: int, skip_down: int) -> int:
    width = 0
    trees = 0
    line_num = -1
    for line in maptext:
        line_num += 1
        if line_num % skip_down != 0:
            continue
        map_line = line.strip()
        if map_line[width % len(map_line)] == '#':
            trees += 1
        width += skip_right
    return trees


def read_stdin(in_stream: TextIO) -> List[str]:
    text = []
    for line in in_stream:
        text.append(line)
    return text


def main() -> None:
    aparser = argparse.ArgumentParser()
    aparser.add_argument("problem", choices=["one", "two"])
    args = aparser.parse_args()
    text = read_stdin(sys.stdin)
    if args.problem == "one":
        print(count_trees(text, 3, 1))
    else:
        total = 1
        for right, down in SLOPES:
            total *= count_trees(text, right, down)
        print(total)


if __name__ == "__main__":
    main()
