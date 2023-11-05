import numpy as np
import os

DATA_PATH = "data/"

EMPTY = 'W'
WALL = 'B'
BULB = 'L'
NUMBERS = ['0', '1', '2', '3', '4']


def _remove_endl(s: str) -> str:
    return s[:-1] if s[-1] == '\n' else s


class Instance:
    def __init__(self, name: str) -> None:
        self._load_from_file(name)
        self._build()

    def __str__(self):
        res = f'Input: {self.input}\n'
        if self.output:
            res += f'Expected output: {self.output}'
        return res

    def print_map(self) -> None:
        print('\n')
        for row in self.map:
            print(''.join(row), end='\n')
        print('\n')

    def _load_from_file(self, name: str) -> None:
        with open(os.path.join(DATA_PATH, f'{name}.txt'), 'r') as f:
            lines = f.readlines()
            if len(lines) == 0:
                raise Exception("File is empty")
            self.input = _remove_endl(lines[0])
            self.output = _remove_endl(lines[1]) if len(lines) > 1 else None

    def _build(self):
        self.n = int(np.sqrt(len(self.input)))
        self.map = np.array(list(self.input)).reshape(self.n, self.n)[::-1]

    def place_bulb(self, bulb: tuple[int, int]) -> None:
        y, x = bulb
        self.map[y, x] = BULB

    def place_char(self, pos: tuple[int, int], char: str) -> None:
        self.map[pos[0], pos[1]] = char

    def neighborhood(self, bulb: tuple[int, int]) -> list[tuple[int, int]]:
        y, x = bulb
        return [pos for pos in [(y, x + 1), (y, x - 1), (y + 1, x), (y - 1, x)]
                if self.map[pos[0], pos[1]] == EMPTY]

    def _get_line(self, start: tuple[int, int], d: tuple[int, int]):
        y, x = start
        dy, dx = d
        line = []
        while 0 <= y < self.n and 0 <= x < self.n and self.map[y, x] == EMPTY:
            line.append((y, x))
            y += dy
            x += dx
        return line

    def get_illuminated(self, bulb: tuple[int, int]) -> list[tuple[int, int]]:
        right = self._get_line(bulb, (0, 1))
        left = self._get_line(bulb, (0, -1))
        down = self._get_line(bulb, (1, 0))
        up = self._get_line(bulb, (-1, 0))
        return right + left + down + up

    def to_string(self) -> str:
        return ''.join(self.map[::-1].flatten())
