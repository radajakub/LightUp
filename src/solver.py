from instance import Instance
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical103
from pysat.formula import IDPool


class Solver:
    def __init__(self, instance: Instance) -> None:
        self.instance = instance
        self.illuminated_to_pos = dict()
        self.illuminated_to_var = dict()
        self.bulb_to_pos = dict()
        self.bulb_to_var = dict()
        self.clauses = []
        self.id_pool = IDPool()
        self._build_representation()

    def print_clauses(self) -> None:
        print(f'CLAUSES:')
        for clause in self.clauses:
            string = '-> ['
            for var in clause:
                if var < 0:
                    string += 'not '
                    var = abs(var)
                if var in self.illuminated_to_pos:
                    string += f'I{self.illuminated_to_pos[var]}, '
                elif var in self.bulb_to_pos:
                    string += f'B{self.bulb_to_pos[var]}, '
            string += ']'
            print(string)

    def print_translations(self) -> None:
        print(f'ILLUMINATED VARS: ')
        for pos, var in self.illuminated_to_var.items():
            print(f'- {pos} -> {var}')
        print(f'BULB VARS: ')
        for pos, var in self.bulb_to_var.items():
            print(f'- {pos} -> {var}')

    def _build_representation(self) -> None:
        self.clauses = []
        # positions which have to be illuminated and where bulb can be places
        empty_positions = self.instance.get_empty()
        # positions of numbers which specify the number of bulbs in the neighborhood
        number_positions = self.instance.get_numbers()

        self._init_variables(empty_positions)

        self._add_illuminated_constraint(empty_positions)
        self._add_bulb_illumination_constraint(empty_positions)
        self._add_two_bulbs_constraint(empty_positions)
        self._add_number_constraint(number_positions)

    def _init_variables(self, empty_positions: list[tuple[int, int]]) -> None:
        var_id = 1
        for pos in empty_positions:
            self.illuminated_to_var[pos] = var_id
            self.illuminated_to_pos[var_id] = pos
            var_id += 1
        for bulb in empty_positions:
            self.bulb_to_pos[var_id] = bulb
            self.bulb_to_var[bulb] = var_id
            var_id += 1
        self.id_pool.occupy(1, var_id - 1)

    def _add_illuminated_constraint(self, illuminated_positions: list[tuple[int, int]]) -> None:
        for pos in illuminated_positions:
            self.clauses.append([self.illuminated_to_var[pos]])

    def _add_bulb_illumination_constraint(self, illuminated_positions: list[tuple[int, int]]) -> None:
        for illuminated in illuminated_positions:
            clause = [-self.illuminated_to_var[illuminated]]
            for pos in self.instance.get_illuminated(illuminated):
                clause.append(self.bulb_to_var[pos])
            self.clauses.append(clause)

    def _add_two_bulbs_constraint(self, bulb_positions: list[tuple[int, int]]) -> None:
        for bulb in bulb_positions:
            bulb_var = self.bulb_to_var[bulb]
            for pos in self.instance.get_illuminated(bulb):
                if bulb != pos:
                    self.clauses.append([-bulb_var, -self.bulb_to_var[pos]])

    def _add_number_constraint(self, number_positions: list[tuple[int, int]]) -> None:
        for num_pos in number_positions:
            k = self.instance.get_num(num_pos)
            vars = [self.bulb_to_var[pos] for pos in self.instance.get_neighborhood(num_pos)]
            card = CardEnc.equals(lits=vars, bound=k, vpool=self.id_pool)
            self.clauses += card.clauses

    def _apply_model(self, model: list[int]) -> None:
        for var in model:
            if var > 0 and var in self.bulb_to_pos:
                pos = self.bulb_to_pos[var]
                self.instance.place_bulb(pos)

    def solve(self) -> None:
        s = Cadical103(bootstrap_with=self.clauses)
        res = s.solve()

        if res:
            model = s.get_model()
            self._apply_model(model)

        return res
