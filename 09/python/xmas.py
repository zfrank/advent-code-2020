#!/usr/bin/env python3

import argparse
from typing import List, TextIO, Tuple
import sys


def find_two_sum(values: List[int], match: int) -> bool:
    if len(values) < 2:
        return False
    for i, x in enumerate(values[:-1]):
        for y in values[i+1:]:
            if x + y == match:
                return True
    return False


def find_multi_sum(values: List[int], match: int) -> Tuple[int, int]:
    for i, x in enumerate(values):
        queue = [x]
        total = x
        for y in values[i+1:]:
            if total + y <= match:
                total += y
                queue.append(y)
                if total == match:
                    return min(queue), max(queue)
            else:
                break
    raise ValueError("No matching values were found in input")


def find_weakness(in_data: List[int], preamble: int) -> int:
    queue = in_data[:preamble]
    for value in in_data[preamble:]:
        if find_two_sum(queue, value):
            queue.append(value)
            queue.pop(0)
        else:
            return value
    raise ValueError("No matching values were found in input")


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
        print(find_weakness(data, 25))
    else:
        weak = find_weakness(data, 25)
        lo, hi = find_multi_sum(data, weak)
        print(lo + hi)


if __name__ == "__main__":
    main()
