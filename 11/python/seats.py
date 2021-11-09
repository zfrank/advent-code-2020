#!/usr/bin/env python3

import argparse
from typing import Dict, List, Optional, TextIO, Tuple
import sys
from enum import Enum


def seats_are_equal(s1: List[str], s2: List[str]) -> bool:
    if len(s1) != len(s2):
        return False
    for row1, row2 in zip(s1, s2):
        if row1 != row2:
            return False
    return True


def count_occupied_seats(seats: List[str]) -> int:
    count = 0
    for row in seats:
        for s in row:
            if s == "#":
                count += 1
    return count


def seat_is_occupied(seats: List[str], x: int, y: int) -> int:
    '''
    Returns 1 if the seat is occupied. Returns 0 otherwise (even if the
    seat is out of bounds).
    '''
    if x < 0 or x >= len(seats):
        return 0
    row = seats[x]
    if y < 0 or y >= len(row):
        return 0
    seat = row[y]
    if seat == '#':
        return 1
    return 0


def check_surround_occupied(seats: List[str], x: int, y: int) -> int:
    '''
    Returns the number of occupied seats ('#') around the seat with
    coordinates x, y. Look at all eight seats around it (up, down, left, right
    and diagonals).
    '''
    return sum([
        seat_is_occupied(seats, x-1, y-1),
        seat_is_occupied(seats, x-1, y),
        seat_is_occupied(seats, x-1, y+1),
        seat_is_occupied(seats, x, y-1),
        seat_is_occupied(seats, x, y+1),
        seat_is_occupied(seats, x+1, y-1),
        seat_is_occupied(seats, x+1, y),
        seat_is_occupied(seats, x+1, y+1),
    ])


class Direction(Enum):
    EAST = 1
    WEST = 2
    NORTH = 3
    SOUTH = 4
    NW = 5
    NE = 6
    SW = 7
    SE = 8


class ViewCache:
    '''
    Store the last seat and its coordinates that was seen on a certain
    direction. This cache assumes that the grid of seats will be traversed from
    top left to bottom right.
    '''

    def __init__(self, h: int, w: int):
        self.max_row = h - 1
        self.max_col = w - 1
        self.data: Dict[str, Tuple[int, int, str]] = {}

    def __repr__(self) -> str:
        return str(self.data)

    def _check_coordinates(self, x: int, y: int) -> None:
        if x < 0 or x > self.max_row:
            raise ValueError(f"Invalid value for x: {x}")
        if y < 0 or y > self.max_col:
            raise ValueError(f"Invalid value for y: {y}")

    def get_diag_id(self, d: Direction, x: int, y: int) -> str:
        '''
        Given a direction and a starting point, return the id of the diagonal
        '''
        self._check_coordinates(x, y)
        if d in (Direction.NW, Direction.SE):
            # find start coordinates
            m = min(x, y)
            startx = x - m
            starty = y - m
            # find end coordinates
            n = min(self.max_row - x, self.max_col - y)
            endx = x + n
            endy = y + n
            return f"{startx}:{starty}-{endx}:{endy}"
        if d in (Direction.NE, Direction.SW):
            # find start coordinates
            m = min(self.max_row - x, y)
            startx = x + m
            starty = x - m
            # find end coordinates
            n = min(x, self.max_col - y)
            endx = x - n
            endy = y + n
            return f"{startx}:{starty}-{endx}:{endy}"
        raise ValueError(f"Invalid Direction {d}")

    def get_value(self, x: int, y: int, d: Direction) -> Optional[Tuple[int, int, str]]:
        '''
        Look in cache for last object seen in a row , column or diagonal in the
        specified direction. Returns the coordinates of the object (x,y) and
        its value.  Return None if there is no entry in the cache or if the
        cached object is in the same coordinates as input.
        '''
        #self._check_coordinates(x, y)
        if d in (Direction.EAST, Direction.WEST):
            result = self.data.get(f"row{x}{d}")
        elif d in (Direction.NORTH, Direction.SOUTH):
            result = self.data.get(f"col{y}{d}")
        else:
            diag = self.get_diag_id(d, x, y)
            result = self.data.get(f"diag{diag}{d}")
        if result is None:
            return None
        # Return None if we're further ahead than the cached value
        cx, cy, value = result
        if d == Direction.EAST:
            if cy <= y:
                return None
        elif d == Direction.SOUTH:
            if cx <= x:
                return None
        # Return None if the cached value is the current location
        if cx == x and cy == y:
            return None
        return cx, cy, value

    def set_value(self, x: int, y: int, d: Direction, value: str) -> None:
        #self._check_coordinates(x, y)
        if d in (Direction.EAST, Direction.WEST):
            self.data[f"row{x}{d}"] = (x, y, value)
        elif d in (Direction.NORTH, Direction.SOUTH):
            self.data[f"col{y}{d}"] = (x, y, value)
        else:
            diag = self.get_diag_id(d, x, y)
            self.data[f"diag{diag}{d}"] = (x, y, value)


def find_seat_horizontal(seats: List[str], vc: ViewCache, x: int, y: int, d: Direction) -> int:
    row = seats[x]
    if d is Direction.EAST:
        cached = vc.get_value(x, y, d)
        if cached:
            _, _, value = cached
            return 1 if value == "#" else 0
        # search to the east
        found = ""
        j = y + 1
        while j < len(row):
            n = row[j]
            if n in ("#", "L"):
                found = n
                break
            j += 1
        # update cache
        if found:
            vc.set_value(x, j, d, found)
        else:
            # set empty value
            vc.set_value(x, j, d, "E")
        return 1 if found == "#" else 0
    if d is Direction.WEST:
        cached = vc.get_value(x, y, d)
        if cached:
            _, _, value = cached
            result = 1 if value == "#" else 0
        else:
            # This row has not found any seat yet
            result = 0
        seat = row[y]
        if seat in ("#", "L"):
            # update cache
            vc.set_value(x, y, d, seat)
        return result
    raise ValueError("Invalid Direction for find_seat_horizontal()")


def find_seat_diagonal_NW_SE(seats: List[str], vc: ViewCache, x: int, y: int, d: Direction) -> int:
    row = seats[x]
    if d is Direction.SE:
        cached = vc.get_value(x, y, d)
        if cached:
            _, _, value = cached
            return 1 if value == "#" else 0
        # search to the south-east
        found = ""
        i = x + 1
        j = y + 1
        while i < len(seats) and j < len(row):
            n = seats[i][j]
            if n in ("#", "L"):
                found = n
                break
            i += 1
            j += 1
        # update cache
        if found:
            vc.set_value(i, j, d, found)
        else:
            # set empty value
            vc.set_value(i-1, j-1, d, "E")
        return 1 if found == "#" else 0
    if d is Direction.NW:
        cached = vc.get_value(x, y, d)
        if cached:
            _, _, value = cached
            result = 1 if value == "#" else 0
        else:
            # This row has not found any seat yet
            result = 0
        seat = seats[x][y]
        if seat in ("#", "L"):
            # update cache
            vc.set_value(x, y, d, seat)
        return result
    raise ValueError("Invalid Direction for find_seat_diagonal_NW_SE()")


def find_seat_diagonal_NE_SW(seats: List[str], vc: ViewCache, x: int, y: int, d: Direction) -> int:
    row = seats[x]
    if d is Direction.SW:
        cached = vc.get_value(x, y, d)
        if cached:
            _, _, value = cached
            return 1 if value == "#" else 0
        # search to the south-west
        found = ""
        i = x + 1
        j = y - 1
        while i < len(seats) and j >= 0:
            n = seats[i][j]
            if n in ("#", "L"):
                found = n
                break
            i += 1
            j -= 1
        # update cache
        if found:
            vc.set_value(i, j, d, found)
        else:
            # set empty value
            vc.set_value(i-1, j+1, d, "E")
        return 1 if found == "#" else 0
    if d is Direction.NE:
        cached = vc.get_value(x, y, d)
        if cached:
            _, _, value = cached
            return 1 if value == "#" else 0
        # search to the north-east
        found = ""
        i = x - 1
        j = y + 1
        while i >= 0 and j < len(row):
            n = seats[i][j]
            if n in ("#", "L"):
                found = n
                break
            i -= 1
            j += 1
        # update cache
        if found:
            vc.set_value(i, j, d, found)
        else:
            # set empty value
            vc.set_value(i+1, j-1, d, "E")
        return 1 if found == "#" else 0
    raise ValueError("Invalid Direction for find_seat_diagonal_NE_SW()")


def find_seat_vertical(seats: List[str], vc: ViewCache, x: int, y: int, d: Direction) -> int:
    if d is Direction.SOUTH:
        cached = vc.get_value(x, y, d)
        if cached:
            _, _, value = cached
            return 1 if value == "#" else 0
        # search to the south
        found = ""
        i = x + 1
        while i < len(seats):
            n = seats[i][y]
            if n in ("#", "L"):
                found = n
                break
            i += 1
        # update cache
        if found:
            vc.set_value(i, y, d, found)
        else:
            # set empty value
            vc.set_value(i, y, d, "E")
        return 1 if found == "#" else 0
    if d is Direction.NORTH:
        cached = vc.get_value(x, y, d)
        if cached:
            _, _, value = cached
            result = 1 if value == "#" else 0
        else:
            # This row has not found any seat yet
            result = 0
        seat = seats[x][y]
        if seat in ("#", "L"):
            # update cache
            vc.set_value(x, y, d, seat)
        return result
    raise ValueError("Invalid Direction for find_seat_vertical()")


def find_seat_by_direction(seats: List[str], vc: ViewCache, x: int, y: int, d: Direction) -> int:
    '''
    Find the first that can be seen in the specified direction, starting from
    seat in coordinates x y. Return 1 if that seat is occupied. Return 0 if the
    seat is empty or no seat is found.
    '''
    if d in (Direction.WEST, Direction.EAST):
        return find_seat_horizontal(seats, vc, x, y, d)
    if d in (Direction.NORTH, Direction.SOUTH):
        return find_seat_vertical(seats, vc, x, y, d)
    if d in (Direction.NW, Direction.SE):
        return find_seat_diagonal_NW_SE(seats, vc, x, y, d)
    if d in (Direction.NE, Direction.SW):
        return find_seat_diagonal_NE_SW(seats, vc, x, y, d)
    raise ValueError("Invalid Direction")


def check_view_occupied(seats: List[str], vc: ViewCache, x: int, y: int) -> int:
    '''
    Returns the number of occupied seats ('#') that can be seen from
    coordinates x, y. Look at all eight directions (up, down, left, right and
    diagonals).
    Always use the same ViewCache object for a certain seats object. Make sure
    to iterate over all seats from top to bottom, left to right.
    '''
    result = 0
    for d in Direction:
        result += find_seat_by_direction(seats, vc, x, y, d)
    return result


def apply_step_one(seats: List[str]) -> List[str]:
    result: List[str] = []
    for i, row in enumerate(seats):
        newrow = []
        for j, seat in enumerate(row):
            if seat == "L" and check_surround_occupied(seats, i, j) == 0:
                newrow.append("#")
            elif seat == "#" and check_surround_occupied(seats, i, j) >= 4:
                newrow.append("L")
            else:
                newrow.append(seat)
        result.append("".join(newrow))
    return result


def apply_step_two(seats: List[str]) -> List[str]:
    result: List[str] = []
    if len(seats) < 1:
        return result
    vc = ViewCache(len(seats), len(seats[0]))
    for i, row in enumerate(seats):
        newrow = []
        for j, seat in enumerate(row):
            # search in all directions
            if seat == "L" and check_view_occupied(seats, vc, i, j) == 0:
                newrow.append("#")
            elif seat == "#" and check_view_occupied(seats, vc, i, j) >= 5:
                newrow.append("L")
            else:
                newrow.append(seat)
        result.append("".join(newrow))
    return result


def run_simulation(seats: List[str], problem: int) -> int:
    before = seats
    if problem == 1:
        step_func = apply_step_one
    else:
        step_func = apply_step_two
    after = step_func(seats)
    while not seats_are_equal(before, after):
        print(".", flush=True, end="")
        before = after
        after = step_func(after)
    return count_occupied_seats(after)


def read_input(in_stream: TextIO) -> List[str]:
    result = []
    for line in in_stream:
        result.append(line.strip())
    return result


def main() -> None:
    aparser = argparse.ArgumentParser()
    aparser.add_argument("problem", choices=["one", "two"])
    args = aparser.parse_args()
    data = read_input(sys.stdin)
    if args.problem == "one":
        print(run_simulation(data, 1))
    else:
        print(run_simulation(data, 2))


if __name__ == "__main__":
    main()
