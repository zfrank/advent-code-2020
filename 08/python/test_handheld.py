#!/usr/bin/env python3

import io
import handheld
import textwrap
import unittest


class TestEmulatorParseLine(unittest.TestCase):
    def test_parse_line(self) -> None:
        inst, param = handheld.Emulator.parse_line("nop +0")
        self.assertEqual("nop", inst)
        self.assertEqual(0, param)


class TestHandheldEmulator(unittest.TestCase):
    def setUp(self) -> None:
        self.text = io.StringIO(textwrap.dedent("""\
		nop +0
		acc +1
		jmp +4
		acc +3
		jmp -3
		acc -99
		acc +1
		jmp -4
		acc +6"""))

    def test_example_one(self) -> None:
        code = handheld.read_input(self.text)
        em = handheld.Emulator(code)
        with self.assertRaises(handheld.InfiniteLoop) as ex:
            em.run()
        self.assertEqual(5, ex.exception.coredump.acc)

    def test_example_two(self) -> None:
        code = handheld.read_input(self.text)
        em = handheld.Emulator(code, True)
        t = em.run()
        self.assertEqual(8, t.acc)


if __name__ == "__main__":
    unittest.main(verbosity=2)
