#!/usr/bin/env python3
import binary_boarding
import unittest


class TestBinaryBoardingOne(unittest.TestCase):
    def test_example_zero(self) -> None:
        self.assertEqual(357, binary_boarding.parse_seat_id("FBFBBFFRLR"))

    def test_example_one(self) -> None:
        self.assertEqual(567, binary_boarding.parse_seat_id("BFFFBBFRRR"))

    def test_example_two(self) -> None:
        self.assertEqual(119, binary_boarding.parse_seat_id("FFFBBBFRRR"))

    def test_example_three(self) -> None:
        self.assertEqual(820, binary_boarding.parse_seat_id("BBFFBBFRLL"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
