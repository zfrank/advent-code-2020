#!/usr/bin/env python3

import io
import haversacks
import textwrap
import unittest


class TestHaversacksParseLine(unittest.TestCase):
    def test_no_other_bags(self) -> None:
        node, neigh = haversacks.parse_line("dotted black bags contain no other bags.")
        self.assertEqual("dotted black", node)
        self.assertEqual([], neigh)

    def test_match_two_bags(self) -> None:
        node, neigh = haversacks.parse_line("light red bags contain 1 bright white bag, 2 muted yellow bags.")
        self.assertEqual("light red", node)
        self.assertEqual([(1, "bright white"), (2, "muted yellow")], neigh)


class TestHaversacksOne(unittest.TestCase):
    def setUp(self) -> None:
        self.text = io.StringIO(textwrap.dedent("""\
        light red bags contain 1 bright white bag, 2 muted yellow bags.
        dark orange bags contain 3 bright white bags, 4 muted yellow bags.
        bright white bags contain 1 shiny gold bag.
        muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
        shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
        dark olive bags contain 3 faded blue bags, 4 dotted black bags.
        vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
        faded blue bags contain no other bags.
        dotted black bags contain no other bags."""))

    def test_build_graphs(self) -> None:
        graph, revgraph = haversacks.build_graphs(self.text)
        self.assertEqual(9, len(graph))
        self.assertEqual(7, len(revgraph))

    def test_example_one(self) -> None:
        _, revgraph = haversacks.build_graphs(self.text)
        self.assertEqual(5, len(haversacks.bfs(revgraph, "shiny gold")))

    def test_example_two(self) -> None:
        graph, _ = haversacks.build_graphs(self.text)
        self.assertEqual(32, haversacks.count_bags(graph, "shiny gold"))


class TestHaversacksTwo(unittest.TestCase):
    def setUp(self) -> None:
        self.text = io.StringIO(textwrap.dedent("""\
		shiny gold bags contain 2 dark red bags.
		dark red bags contain 2 dark orange bags.
		dark orange bags contain 2 dark yellow bags.
		dark yellow bags contain 2 dark green bags.
		dark green bags contain 2 dark blue bags.
		dark blue bags contain 2 dark violet bags.
		dark violet bags contain no other bags."""))

    def test_example_two_extra(self) -> None:
        graph, _ = haversacks.build_graphs(self.text)
        self.assertEqual(126, haversacks.count_bags(graph, "shiny gold"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
