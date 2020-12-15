#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict
from typing import Set, List, TextIO

def parse_line_one(group: Set[str], line: str, start: bool) -> Set[str]:
    for char in line:
        group.add(char)
    return group


def parse_line_two(group: Set[str], line: str, start: bool) -> Set[str]:
    answers = set(line)
    # If a new group just started, then "group" will be empty.
    # Accept all the values from line to initialise the count.
    if start:
        return answers
    # set intersection
    return group & answers


def parser(in_stream: TextIO, problem: str) -> List[Set[str]]:
    groups = []
    if problem == "one":
        parse_line = parse_line_one
    else:
        parse_line = parse_line_two
    start = True
    new_group = set()
    for line in in_stream:
        line = line.strip()
        if not line:
            groups.append(new_group)
            # start new group
            start = True
            new_group = set()
        else:
            new_group = parse_line(new_group, line, start)
            if start:
                start = False
    # add the last group
    groups.append(new_group)
    return groups


def count_answers(groups: List[Set[str]]):
    return sum([len(x) for x in groups])


def main():
    aparser = argparse.ArgumentParser()
    aparser.add_argument("problem", choices=["one", "two"])
    args = aparser.parse_args()
    groups = parser(sys.stdin, args.problem)
    print(count_answers(groups))


if __name__ == '__main__':
    main()
