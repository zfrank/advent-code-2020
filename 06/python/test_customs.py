#!/usr/bin/env python3

import io
import textwrap
import customs
import unittest


class TestCustoms(unittest.TestCase):
    def setUp(self) -> None:
        self.text = io.StringIO(textwrap.dedent("""\
        abc

        a
        b
        c

        ab
        ac

        a
        a
        a
        a

        b"""))

    def test_example_one(self) -> None:
        self.assertEqual(11, customs.count_answers(customs.parser(self.text, "one")))

    def test_example_two(self) -> None:
        self.assertEqual(6, customs.count_answers(customs.parser(self.text, "two")))


if __name__ == '__main__':
    unittest.main(verbosity=2)
