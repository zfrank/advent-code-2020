#!/usr/bin/env python3

import io
import textwrap
import unittest
import seats


class TestViewCache(unittest.TestCase):
    def setUp(self) -> None:
        self.vc = seats.ViewCache(5, 7)

    def test_get_diag_id(self) -> None:
        self.assertEqual("0:1-4:5", self.vc.get_diag_id(seats.Direction.NW, 3, 4))
        self.assertEqual("0:1-4:5", self.vc.get_diag_id(seats.Direction.SE, 3, 4))
        self.assertEqual("4:2-1:6", self.vc.get_diag_id(seats.Direction.NE, 3, 4))
        self.assertEqual("4:2-1:6", self.vc.get_diag_id(seats.Direction.SW, 3, 4))

    def test_get_value_empty(self) -> None:
        self.assertIsNone(self.vc.get_value(3, 4, seats.Direction.EAST))

    def test_set_value_and_get_east(self) -> None:
        self.vc.set_value(3, 4, seats.Direction.EAST, "#")
        self.assertEqual((3, 4, "#"), self.vc.get_value(3, 3, seats.Direction.EAST))
        self.assertEqual((3, 4, "#"), self.vc.get_value(3, 0, seats.Direction.EAST))
        self.assertIsNone(self.vc.get_value(3, 4, seats.Direction.EAST))

    def test_set_value_and_get_west(self) -> None:
        self.vc.set_value(3, 3, seats.Direction.WEST, "L")
        self.assertEqual((3, 3, "L"), self.vc.get_value(3, 4, seats.Direction.WEST))
        self.assertEqual((3, 3, "L"), self.vc.get_value(3, 6, seats.Direction.WEST))
        self.assertIsNone(self.vc.get_value(3, 3, seats.Direction.WEST))


class TestFindSeatH(unittest.TestCase):
    def setUp(self) -> None:
        text = io.StringIO(textwrap.dedent("""\
        .L.L.#.#.#.#."""))
        self.values = seats.read_input(text)
        self.vc = seats.ViewCache(len(self.values), len(self.values[0]))

    def test_find_seat_horizontal_east(self) -> None:
        self.assertEqual(
            0,
            seats.find_seat_horizontal(self.values, self.vc, 0, 0, seats.Direction.EAST),
        )
        self.assertEqual(
            0,
            seats.find_seat_horizontal(self.values, self.vc, 0, 0, seats.Direction.WEST),
        )
        self.assertEqual(
            1,
            seats.find_seat_horizontal(self.values, self.vc, 0, 3, seats.Direction.EAST),
        )

    def test_find_seat_horizontal_west(self) -> None:
        self.assertEqual(
            0,
            seats.find_seat_horizontal(self.values, self.vc, 0, 0, seats.Direction.WEST),
        )
        self.assertEqual(
            0,
            seats.find_seat_horizontal(self.values, self.vc, 0, 5, seats.Direction.WEST),
        )
        self.assertEqual(
            1,
            seats.find_seat_horizontal(self.values, self.vc, 0, 6, seats.Direction.WEST),
        )


class TestFindSeatV(unittest.TestCase):
    def setUp(self) -> None:
        text = io.StringIO(textwrap.dedent("""\
        .L.L.
        .L.#.
        .L.L."""))
        self.values = seats.read_input(text)
        self.vc = seats.ViewCache(len(self.values), len(self.values[0]))

    def test_find_seat_vertical_south(self) -> None:
        self.assertEqual(
            0,
            seats.find_seat_vertical(self.values, self.vc, 0, 0, seats.Direction.SOUTH),
        )
        self.assertEqual(
            1,
            seats.find_seat_vertical(self.values, self.vc, 0, 3, seats.Direction.SOUTH),
        )
        self.assertEqual(
            0,
            seats.find_seat_vertical(self.values, self.vc, 2, 3, seats.Direction.SOUTH),
        )

    def test_find_seat_vertical_north(self) -> None:
        self.assertEqual(
            0,
            seats.find_seat_vertical(self.values, self.vc, 0, 3, seats.Direction.NORTH),
        )
        self.assertEqual(
            0,
            seats.find_seat_vertical(self.values, self.vc, 1, 3, seats.Direction.NORTH),
        )
        self.assertEqual(
            1,
            seats.find_seat_vertical(self.values, self.vc, 2, 3, seats.Direction.NORTH),
        )


class TestFindSeatDiagonal(unittest.TestCase):
    def setUp(self) -> None:
        text = io.StringIO(textwrap.dedent("""\
        .L.L.#.#.
        .L.#.#.#.
        .L.L.#.#."""))
        self.values = seats.read_input(text)
        self.vc = seats.ViewCache(len(self.values), len(self.values[0]))

    def test_find_seat_diagonal_se(self) -> None:
        self.assertEqual(
            1,
            seats.find_seat_diagonal_NW_SE(self.values, self.vc, 0, 2, seats.Direction.SE),
        )
        self.assertEqual(
            0,
            seats.find_seat_diagonal_NW_SE(self.values, self.vc, 1, 3, seats.Direction.SE),
        )
        self.assertEqual(
            0,
            seats.find_seat_diagonal_NW_SE(self.values, self.vc, 2, 4, seats.Direction.SE),
        )

    def test_find_seat_diagonal_nw(self) -> None:
        self.assertEqual(
            0,
            seats.find_seat_diagonal_NW_SE(self.values, self.vc, 0, 2, seats.Direction.NW),
        )
        self.assertEqual(
            0,
            seats.find_seat_diagonal_NW_SE(self.values, self.vc, 1, 3, seats.Direction.NW),
        )
        self.assertEqual(
            1,
            seats.find_seat_diagonal_NW_SE(self.values, self.vc, 2, 4, seats.Direction.NW),
        )

    def test_find_seat_diagonal_ne(self) -> None:
        self.assertEqual(
            0,
            seats.find_seat_diagonal_NE_SW(self.values, self.vc, 0, 0, seats.Direction.NE),
        )
        self.assertEqual(
            0,
            seats.find_seat_diagonal_NE_SW(self.values, self.vc, 1, 1, seats.Direction.NE),
        )
        self.assertEqual(
            1,
            seats.find_seat_diagonal_NE_SW(self.values, self.vc, 2, 2, seats.Direction.NE),
        )


class TestSeats(unittest.TestCase):
    def setUp(self) -> None:
        text = io.StringIO(textwrap.dedent("""\
        L.LL.LL.LL
        LLLLLLL.LL
        L.L.L..L..
        LLLL.LL.LL
        L.LL.LL.LL
        L.LLLLL.LL
        ..L.L.....
        LLLLLLLLLL
        L.LLLLLL.L
        L.LLLLL.LL"""))
        self.values = seats.read_input(text)

        r1 = io.StringIO(textwrap.dedent("""\
        #.##.##.##
        #######.##
        #.#.#..#..
        ####.##.##
        #.##.##.##
        #.#####.##
        ..#.#.....
        ##########
        #.######.#
        #.#####.##"""))
        self.round_one = seats.read_input(r1)

    def test_round_one(self) -> None:
        self.assertTrue(
            seats.seats_are_equal(self.round_one, seats.apply_step_one(self.values)))

    def test_part_one(self) -> None:
        self.assertEqual(37, seats.run_simulation(self.values, 1))

    def test_part_two(self) -> None:
        self.assertEqual(26, seats.run_simulation(self.values, 2))


if __name__ == "__main__":
    unittest.main(verbosity=2)
