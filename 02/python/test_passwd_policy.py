#!/usr/bin/env python3

import unittest
import passwd_policy


class TestParseLine(unittest.TestCase):
    def test_parse_line(self) -> None:
        pol, passwd = passwd_policy.parse_line("4-6 v: vvvvvqvvv")
        self.assertEqual("vvvvvqvvv", passwd)
        self.assertEqual(4, pol.min)
        self.assertEqual(6, pol.max)
        self.assertEqual("v", pol.char)


class TestPasswdPolicyCount(unittest.TestCase):
    def test_policy_no_match_too_many(self) -> None:
        p = passwd_policy.Policy("4-6 v")
        self.assertFalse(p.match_count("vvvvvqvvv"))

    def test_policy_no_match_too_few(self) -> None:
        p = passwd_policy.Policy("4-6 q")
        self.assertFalse(p.match_count("vvvvvqvvv"))

    def test_policy_match(self) -> None:
        p = passwd_policy.Policy("4-6 v")
        self.assertTrue(p.match_count("vvvqvvv"))


class TestPasswdPolicyPosition(unittest.TestCase):
    def test_policy_no_match(self) -> None:
        p = passwd_policy.Policy("2-9 c")
        self.assertFalse(p.match_pos("ccccccccc"))

    def test_policy_match(self) -> None:
        p = passwd_policy.Policy("1-3 a")
        self.assertTrue(p.match_pos("abcde"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
