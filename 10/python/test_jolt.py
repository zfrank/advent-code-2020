#!/usr/bin/env python3

import io
import textwrap
import unittest
import jolt


class TestExampleOne(unittest.TestCase):
    def setUp(self) -> None:
        text = io.StringIO(textwrap.dedent("""\
        16
        10
        15
        5
        1
        11
        7
        19
        6
        12
        4"""))
        self.values = jolt.read_input(text)

    def test_part_one(self) -> None:
        self.assertEqual((7, 5), jolt.get_diffs(self.values))

    def test_part_two(self) -> None:
        self.assertEqual(8, jolt.find_all_paths(self.values))


class TestExampleTwo(unittest.TestCase):
    def setUp(self) -> None:
        text = io.StringIO(textwrap.dedent("""\
        28
        33
        18
        42
        31
        14
        46
        20
        48
        47
        24
        23
        49
        45
        19
        38
        39
        11
        1
        32
        25
        35
        8
        17
        7
        9
        4
        2
        34
        10
        3"""))
        self.values = jolt.read_input(text)

    def test_part_one(self) -> None:
        self.assertEqual((22, 10), jolt.get_diffs(self.values))

    def test_part_two(self) -> None:
        self.assertEqual(19208, jolt.find_all_paths(self.values))


if __name__ == "__main__":
    unittest.main(verbosity=2)
