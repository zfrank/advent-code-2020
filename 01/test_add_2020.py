#!/usr/bin/env python3

import unittest
import add_2020


class TestAdd2020(unittest.TestCase):
    def test_add_2020_two(self):
        got = add_2020.add2020Two([1721, 979, 366, 299, 675, 1456])
        expected = (1721, 299)
        self.assertEqual(expected, got)

    def test_add_2020_three(self):
        got = add_2020.add2020Three([1721, 979, 366, 299, 675, 1456])
        expected = (979, 366, 675)
        self.assertEqual(expected, got)


if __name__ == '__main__':
    unittest.main(verbosity=2)
