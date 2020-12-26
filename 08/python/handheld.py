#!/usr/bin/env python3

# this import can be removed in python 3.10
# https://www.python.org/dev/peps/pep-0563/
from __future__ import annotations
import argparse
import sys
from typing import List, NamedTuple, Optional, Set, TextIO, Tuple


CoreDump = NamedTuple("CoreDump", [("acc", int), ("ip", int)])


class EmulatorError(Exception):
    def __init__(self, coredump: CoreDump) -> None:
        self.coredump = coredump
        super().__init__()


class InfiniteLoop(EmulatorError):
    pass


class UnknownInst(EmulatorError):
    pass


class Thread:
    def __init__(self, start: int = 0, acc: int = 0, visited: Optional[Set[int]] = None) -> None:
        self.ip = start
        self.acc = acc
        self.visited: Set[int] = visited or set()

    def clone(self) -> Thread:
        return Thread(self.ip, self.acc, self.visited.copy())

    def make_coredump(self) -> CoreDump:
        return CoreDump(self.acc, self.ip)


class Emulator:
    def __init__(self, code: List[str], nopjmp_switch: bool = False) -> None:
        self.code = code
        self.nopjmp_switch = nopjmp_switch

    def _run_instruction(self, t: Thread, can_clone: bool = False) -> Optional[Thread]:
        if t.ip in t.visited:
            raise InfiniteLoop(t.make_coredump())

        result = None
        t.visited.add(t.ip)
        inst, param = Emulator.parse_line(self.code[t.ip])
        if inst == "acc":
            t.acc += param
            t.ip += 1
        elif inst == "jmp":
            if can_clone:
                result = t.clone()
                result.ip += 1
            t.ip += param
        elif inst == "nop":
            if can_clone:
                result = t.clone()
                result.ip += param
            t.ip += 1
        else:
            raise UnknownInst(t.make_coredump())
        return result

    @staticmethod
    def parse_line(line: str) -> Tuple[str, int]:
        inst, param = line.split(" ")
        return inst, int(param)

    def _run_simple(self, t: Thread) -> None:
        while t.ip < len(self.code):
            self._run_instruction(t)

    def _run_multithread(self, t: Thread) -> Thread:
        while t.ip < len(self.code):
            alt = self._run_instruction(t, True)
            if alt:
                try:
                    self._run_simple(alt)
                except InfiniteLoop:
                    # ignore this branch
                    pass
                else:
                    # this branch succeeded!
                    return alt
        return t

    def run(self) -> Thread:
        t = Thread()
        if not self.nopjmp_switch:
            self._run_simple(t)
            return t
        return self._run_multithread(t)


def read_input(in_stream: TextIO) -> List[str]:
    return [line.strip() for line in in_stream]


def main() -> None:
    aparser = argparse.ArgumentParser()
    aparser.add_argument("problem", choices=["one", "two"])
    args = aparser.parse_args()
    program = read_input(sys.stdin)
    if args.problem == "one":
        em = Emulator(program)
        try:
            em.run()
        except InfiniteLoop as ex:
            print(ex.coredump.acc)
    else:
        em = Emulator(program, True)
        t = em.run()
        print(t.acc)


if __name__ == "__main__":
    main()
