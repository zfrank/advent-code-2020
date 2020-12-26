#!/usr/bin/env python3

import io
import textwrap
import trajectory
import unittest


class TestTrajectory(unittest.TestCase):
    def setUp(self) -> None:
        text_src = io.StringIO(textwrap.dedent("""\
        ..##.......
        #...#...#..
        .#....#..#.
        ..#.#...#.#
        .#...##..#.
        ..#.##.....
        .#.#.#....#
        .#........#
        #.##...#...
        #...##....#
        .#..#...#.#"""))
        self.text = trajectory.read_stdin(text_src)

    def test_example_three_one(self) -> None:
        self.assertEqual(7, trajectory.count_trees(self.text, 3, 1))

    def test_example_one_one(self) -> None:
        self.assertEqual(2, trajectory.count_trees(self.text, 1, 1))

    def test_example_one_two(self) -> None:
        self.assertEqual(2, trajectory.count_trees(self.text, 1, 2))


if __name__ == '__main__':
    unittest.main(verbosity=2)
