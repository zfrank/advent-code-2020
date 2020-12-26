#!/usr/bin/env python3

import argparse
import sys


def binary_search(code: str, hi: int, lo: int, hi_code: str) -> int:
    for step in code:
        if step == hi_code:
            lo = lo + ((hi - lo) // 2) + 1
        else:
            hi = lo + ((hi - lo) // 2)
    if hi != lo:
        raise ValueError(f"Invalid seat: {code}. min: {lo}. max: {hi}")
    return hi


def parse_seat_id(seat_id: str) -> int:
    row_code = seat_id[:7]
    col_code = seat_id[7:]
    row = binary_search(row_code, 127, 0, "B")
    col = binary_search(col_code, 7, 0, "R")
    return (row * 8) + col


def main() -> None:
    aparser = argparse.ArgumentParser()
    aparser.add_argument("problem", choices=["one", "two"])
    args = aparser.parse_args()
    if args.problem == "one":
        max_seat_id = -1
        for line in sys.stdin:
            seat_id = parse_seat_id(line.strip())
            max_seat_id = max([max_seat_id, seat_id])
        print(max_seat_id)
    else:
        # find the gap in the list of seats
        seats = []
        for line in sys.stdin:
            seats.append(parse_seat_id(line.strip()))
        sorted_seats = sorted(seats)
        prev = sorted_seats[0]
        for s in sorted_seats[1:]:
            if s != prev + 1:
                print(prev + 1)


if __name__ == '__main__':
    main()
