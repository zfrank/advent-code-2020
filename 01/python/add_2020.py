#!/usr/bin/env python3

from typing import List, Tuple
import argparse
import textwrap
import sys


def add2020Two(num_list: List[int]) -> Tuple[int, int]:
    for i, num1 in enumerate(num_list[:-1]):
        for num2 in num_list[i+1:]:
            if num1 + num2 == 2020:
                return (num1, num2)
    raise ValueError("No valid results in num_list")


def add2020Three(num_list: List[int]) -> Tuple[int, int, int]:
    for i, num1 in enumerate(num_list[:-2]):
        for j, num2 in enumerate(num_list[i+1:-1]):
            for _, num3 in enumerate(num_list[i+j+1:]):
                if num1 + num2 + num3 == 2020:
                    return (num1, num2, num3)
    raise ValueError("No valid results in num_list")


def main() -> None:
    aparser = argparse.ArgumentParser(
        description=textwrap.dedent("""\
        Read a list of numbers from stdin and find the combination of two or
        three numbers add up to 2020 and multiply them together."""))
    aparser.add_argument("problem", choices=["one", "two"])
    args = aparser.parse_args()
    num_list = []
    for line in sys.stdin:
        num_list.append(int(line.strip()))
    if args.problem == "one":
        num1, num2 = add2020Two(num_list)
        print(num1, num2)
        print(num1 * num2)
    else:
        num1, num2, num3 = add2020Three(num_list)
        print(num1, num2, num3)
        print(num1 * num2 * num3)


if __name__ == "__main__":
    main()
