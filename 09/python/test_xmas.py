#!/usr/bin/env python3

import io
import textwrap
import unittest
import xmas


class TestFindTwoSum(unittest.TestCase):
    def test_find_two_sum_match(self) -> None:
        self.assertTrue(xmas.find_two_sum([35, 20, 15, 25, 47], 40))

    def test_find_two_sum_no_match(self) -> None:
        self.assertFalse(xmas.find_two_sum([95, 102, 117, 150, 182], 127))


class TestFindMultiSum(unittest.TestCase):
    def test_find_multi_sum_match(self) -> None:
        self.assertEqual((15, 47), xmas.find_multi_sum([15, 25, 47, 40], 127))


class TestXmasOne(unittest.TestCase):
    def setUp(self) -> None:
        text = io.StringIO(textwrap.dedent("""\
		35
		20
		15
		25
		47
		40
		62
		55
		65
		95
		102
		117
		150
		182
		127
		219
		299
		277
		309
		576"""))
        self.values = xmas.read_input(text)

    def test_example_one(self) -> None:
        self.assertEqual(127, xmas.find_weakness(self.values, 5))

    def test_example_two(self) -> None:
        weak = xmas.find_weakness(self.values, 5)
        lo, hi = xmas.find_multi_sum(self.values, weak)
        self.assertEqual(62, lo + hi)


if __name__ == "__main__":
    unittest.main(verbosity=2)
