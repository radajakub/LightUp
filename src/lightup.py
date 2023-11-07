#!/usr/bin/python3

from instance import Instance
from solver import Solver

# set to '' for stdin (i.e. for submission)
INSTANCE = '01'

if __name__ == '__main__':

    instance = Instance(INSTANCE)

    if INSTANCE != '':
        instance.print_map()

    solver = Solver(instance)
    solver._build_representation()

    sat = solver.solve()

    if sat:
        if INSTANCE != '':
            instance.print_map()
            instance.verify()
        else:
            print(instance.to_string())
    else:
        if INSTANCE != '':
            print('UNSAT')
        else:
            print('0')
