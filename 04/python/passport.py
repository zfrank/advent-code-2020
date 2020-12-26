#!/usr/bin/env python3

import argparse
import sys
import re
from typing import Any, Dict, TextIO

RANGES = {
    'byr': (1920, 2002),
    'iyr': (2010, 2020),
    'eyr': (2020, 2030),
    "hgt_cm": (150, 193),
    "hgt_in": (59, 76),
}

EYE_COLOR = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
HAIR_COLOR = "#[0-9a-f]{6}"
HEIGHT_POST = {"cm", "in"}


def validate_range(field: str, value: str) -> bool:
    num_value = int(value)
    lo, hi = RANGES[field]
    return lo <= num_value <= hi


def validate_byr(value: str) -> bool:
    return validate_range("byr", value)


def validate_iyr(value: str) -> bool:
    return validate_range("iyr", value)


def validate_eyr(value: str) -> bool:
    return validate_range("eyr", value)


def validate_hgt(value: str) -> bool:
    prefix = value[:-2]
    postfix = value[-2:]
    if postfix not in HEIGHT_POST:
        return False
    return validate_range(f"hgt_{postfix}", prefix)


def validate_hcl(value: str) -> bool:
    return re.match(HAIR_COLOR, value) is not None


def validate_ecl(value: str) -> bool:
    return value in EYE_COLOR


def validate_pid(value: str) -> bool:
    try:
        int(value)
    except ValueError:
        return False
    return len(value) == 9


class Passport:
    valid_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}
    validate_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

    def __init__(self) -> None:
        self.fields: Dict[str, Any] = {}

    def parse_line(self, line: str) -> None:
        for token in line.split(' '):
            key, value = token.split(':')
            if key not in Passport.valid_fields:
                raise ValueError(f"Invalid field: {key}")
            self.fields[key] = value

    def is_valid(self, problem: str) -> bool:
        if problem == "one":
            return self._is_valid_one()
        return self._is_valid_one() and self._is_valid_two()

    def _is_valid_one(self) -> bool:
        if len(self.fields.keys()) == 8:
            return True
        if len(self.fields.keys()) == 7:
            if 'cid' not in self.fields:
                return True
        return False

    def _is_valid_two(self) -> bool:
        glb = globals()
        for field in Passport.validate_fields:
            validate_func = glb[f"validate_{field}"]
            if not validate_func(self.fields[field]):
                return False
        return True


def parser(in_stream: TextIO, problem: str) -> int:
    passports = []
    count_valid = 0
    new_passp = Passport()
    for line in in_stream:
        line = line.strip()
        if not line:
            # start new passport
            passports.append(new_passp)
            if new_passp.is_valid(problem):
                count_valid += 1
            new_passp = Passport()
        else:
            new_passp.parse_line(line)
    # finish last passport
    passports.append(new_passp)
    if new_passp.is_valid(problem):
        count_valid += 1
    return count_valid


def main() -> None:
    aparser = argparse.ArgumentParser()
    aparser.add_argument("problem", choices=["one", "two"])
    args = aparser.parse_args()
    print(parser(sys.stdin, args.problem))


if __name__ == '__main__':
    main()
