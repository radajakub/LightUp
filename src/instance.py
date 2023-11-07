import numpy as np
from typing import Callable
import os
import itertools

DATA_PATH = "data/"

EMPTY = 'W'
WALL = 'B'
BULB = 'L'
ILLUMINATED = '*'
NUMBERS = ['0', '1', '2', '3', '4']
DIFFS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def _remove_endl(s: str) -> str:
    return s[:-1] if s[-1] == '\n' else s


def _add_pos(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    return tuple(map(sum, zip(p1, p2)))


class Instance:
    @staticmethod
    def show(map: np.ndarray) -> None:
        print('\n')
        for row in map:
            print(''.join(row), end='\n')
        print('\n')

    def __init__(self, name: str) -> None:
        if name == '':
            self._load_from_stdin()
        else:
            self._load_from_file(name)
        self._build()
        self.reset()

    def __str__(self):
        res = f'Input: {self.input}\n'
        if self.output:
            res += f'Expected output: {self.output}'
        return res

    def print_orig_map(self) -> None:
        Instance.show(self.orig_map)

    def print_map(self) -> None:
        Instance.show(self.map)

    def _load_from_stdin(self) -> None:
        self.input = input()

    def _load_from_file(self, name: str) -> None:
        with open(os.path.join(DATA_PATH, f'{name}.txt'), 'r') as f:
            lines = f.readlines()
            if len(lines) == 0:
                raise Exception("File is empty")
            self.input = _remove_endl(lines[0])
            self.output = _remove_endl(lines[1]) if len(lines) > 1 else None

    def _build(self) -> None:
        self.n = int(np.sqrt(len(self.input)))
        self.orig_map = np.array(list(self.input)).reshape(self.n, self.n)[::-1]

    def _place_char(self, pos: tuple[int, int], char: str) -> None:
        self.map[pos[0], pos[1]] = char

    def _is_empty(self, pos: tuple[int, int]) -> bool:
        return self.map[pos[0], pos[1]] == EMPTY

    def _is_number(self, pos: tuple[int, int]) -> bool:
        return self.map[pos[0], pos[1]] in NUMBERS

    def _is_bulb(self, pos: tuple[int, int]) -> bool:
        return self.map[pos[0], pos[1]] == BULB

    def _is_in_range(self, pos: tuple[int, int]) -> bool:
        return 0 <= pos[0] < self.n and 0 <= pos[1] < self.n

    def _get_line(self, pos: tuple[int, int], d: tuple[int, int]) -> list[tuple[int, int]]:
        line = []
        pos = _add_pos(pos, d)
        while self._is_in_range(pos) and self._is_empty(pos):
            line.append(pos)
            pos = _add_pos(pos, d)
        return line

    def _get_positions(self, method: Callable[[tuple[int, int]], bool]) -> list[tuple[int, int]]:
        return [(y, x)
                for y in range(self.n)
                for x in range(self.n)
                if method((y, x))]

    def reset(self) -> None:
        self.map = self.orig_map.copy()

    def place_bulb(self, bulb: tuple[int, int], show_rays: bool = False) -> None:
        self._place_char(bulb, BULB)
        if show_rays:
            for illuminated in self.get_illuminated(bulb):
                if not self._is_bulb(illuminated):
                    self._place_char(illuminated, ILLUMINATED)

    def get_num(self, pos: tuple[int, int]) -> int:
        if self._is_number(pos):
            return int(self.map[pos[0], pos[1]])
        else:
            raise Exception(f'Position {pos} is not a number')

    def get_neighborhood(self, bulb: tuple[int, int]) -> list[tuple[int, int]]:
        return [pos for pos in [_add_pos(bulb, d) for d in DIFFS]
                if self._is_in_range(pos) and self._is_empty(pos)]

    def get_empty(self) -> list[tuple[int, int]]:
        return self._get_positions(self._is_empty)

    def get_numbers(self) -> list[tuple[int, int]]:
        return self._get_positions(self._is_number)

    def get_illuminated(self, bulb: tuple[int, int]) -> list[tuple[int, int]]:
        dirs = [[bulb]] + [self._get_line(bulb, d) for d in DIFFS]
        return list(itertools.chain.from_iterable(dirs))

    def to_string(self) -> str:
        return ''.join(self.map[::-1].flatten())

    def verify(self) -> None:
        if self.to_string() == self.output:
            print('OK')
        else:
            print('WRONG')
