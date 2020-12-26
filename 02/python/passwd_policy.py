#!/usr/bin/env python3

import argparse
import textwrap
import sys
from typing import Tuple


class Policy:
    def __init__(self, raw_str: str):
        # Expected raw_str format:
        #   "range character"
        # Example:
        #   "6-8 g"
        num_range, char = raw_str.split(' ')
        min_str, max_str = num_range.split('-')
        self.min = int(min_str)
        self.max = int(max_str)
        self.char = char
        if self.min >= self.max:
            raise ValueError("Min must be smaller than Max")

    def match_count(self, passwd: str) -> bool:
        # Interpret the numbers in policy as a range.
        # That's the number of occurrences that char is allowed to have in
        # the password.
        counter = 0
        for c in passwd:
            if c == self.char:
                counter += 1
        return self.min <= counter <= self.max

    def match_pos(self, passwd: str) -> bool:
        # Interpret the numbers in policy as positions.
        # The char must appear in one or the other, but not both
        return (passwd[self.min-1] == self.char) != (passwd[self.max-1] == self.char)


def parse_line(line: str) -> Tuple[Policy, str]:
    # Expected line format:
    #   range character: text
    # Example:
    #   4-6 v: vvvvvqvvv
    polstr, passwd = line.split(': ')
    return Policy(polstr), passwd


def main() -> None:
    aparser = argparse.ArgumentParser(
        description=textwrap.dedent("""\
        Read a list of policies and passwords from stdin and count how many
        passwords match their policies."""))
    aparser.add_argument("problem", choices=["one", "two"])
    args = aparser.parse_args()
    if args.problem == "one":
        method_name = "match_count"
    else:
        method_name = "match_pos"

    count = 0
    for line in sys.stdin:
        try:
            policy, passwd = parse_line(line.strip())
        except ValueError:
            print(f"Could not parse this line: {line}", file=sys.stderr)
            sys.exit(1)
        func = getattr(policy, method_name)
        if func(passwd):
            count += 1
    print(count)


if __name__ == "__main__":
    main()
