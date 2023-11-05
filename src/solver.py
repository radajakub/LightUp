from instance import Instance
import pysat as pst
import numpy as np


class Solver:
    def __init__(self, instance: Instance) -> None:
        self.instance = instance

    def build_representation(self) -> None:
        pass

    def solve(self) -> None:
        pass
