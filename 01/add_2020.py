#!/usr/bin/env python3

from typing import List, Optional, Tuple
import sys


def add2020Two(num_list: List[int]) -> Optional[Tuple[int, int]]:
    for i, num1 in enumerate(num_list[:-1]):
        for num2 in num_list[i+1:]:
            if num1 + num2 == 2020:
                return (num1, num2)
    return None


def add2020Three(num_list: List[int]) -> Optional[Tuple[int, int, int]]:
    num_index = list(enumerate(num_list))
    for i, num1 in num_index[:-2]:
        for j, num2 in num_index[i+1:-1]:
            for z, num3 in num_index[j+1:]:
                if num1 + num2 + num3 == 2020:
                    return (num1, num2, num3)
    return None


def fail():
    print("You must specify one paramter: '2' or '3'.", file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        fail()
    param = sys.argv[1]
    if param not in ['2', '3']:
        fail()
    num_list = []
    for line in sys.stdin:
        num_list.append(int(line.strip()))
    if param == '2':
        num1, num2 = add2020Two(num_list)
        print(num1, num2)
        print(num1 * num2)
    else:
        num1, num2, num3 = add2020Three(num_list)
        print(num1, num2, num3)
        print(num1 * num2 * num3)


if __name__ == "__main__":
    main()
