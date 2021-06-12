"""
CSMM.101X - Columbia University - Artificial Intelligence - Week 7 Project - SUDOKU
"""
# Import necessary libraries
from collections import defaultdict, deque
from copy import deepcopy


class Sudoku:

    __slots__ = ('repr_string', 'puzzle', 'solved_puzzle',
                 'unassigned_cells', 'is_solved', 'csp')

    def __init__(self, board_representation=None):
        self.repr_string = board_representation
        self.csp = None
        self.unassigned_cells = set()
        self.puzzle = defaultdict(int)
        self.solved_puzzle = None
        self.is_solved = False
        self.gen_puzzle_from_representation()

    def gen_puzzle_from_representation(self):

        k = 0

        for row in 'ABCDEFGHI':
            for column in '123456789':
                self.puzzle[row + column] = int(self.repr_string[k])

                if int(self.repr_string[k]) == 0:
                    self.unassigned_cells.add(row + column)
                k += 1

    def get_unassigned_cells(self):

        return self.unassigned_cells

    def index_is_valid(self, index):

        if not isinstance(index, str):
            return False

        if len(index) < 2:
            return False

        row_range = lambda x: ord(x) in range(ord('A'), ord('J'))
        column_range = lambda y: int(y) in range(1, 10)

        return row_range(index[0]) and column_range(index[1])

    def is_value_valid(self, value):
        return 1 <= value <= 9

    def get_cell(self, index):

        if self.index_is_valid(index):
            return self.puzzle[index]

        raise ValueError(f"{index} is not a valid puzzle index")

    def set_cell(self, index, value):
        """
            index: Index is row (A..I) + col (1..9)
        """
        if self.index_is_valid(index) and self.is_value_valid(value):
            self.puzzle[index] = value
        raise ValueError(f"{index} is not a valid puzzle index")

    def all_cells(self):
        return self.puzzle.keys()

    def reassign_puzzle(self):

        for key, val in self.csp.domain.items():

            if len(val) == 1:
                self.puzzle[key] = val[0]

    def puzzle_to_str(self):
        ordered_values = []

        for row in 'ABCDEFGHI':
            for column in '123456789':
                ordered_values.append(self.puzzle[row + column])
        return ''.join(str(val) for val in ordered_values)

    def __str__(self):
        return self.puzzle_to_str()

    def revise(self, Xi, Xj):
        revised = False

        for x in self.csp.domain[Xi]:

            if not any(y != x for y in self.csp.domain[Xj]):
                self.csp.domain[Xi].remove(x)
                revised = True

        return revised

    def a3c_solver(self):

        queue = deque(self.csp.binary_constraints)

        while queue:
            Xi, Xj = queue.popleft()

            if self.revise(Xi, Xj):
                if len(self.csp.domain[Xi]) == 0:

                    return self.csp, False

                for X in self.csp.get_neighbor_cells(Xi, Xj):
                    queue.append((X, Xi))

        return self.csp, True

    def solve_with_ac3(self):

        self.csp = SudokuCSP(self)
        self.csp, _ = self.a3c_solver()
        self.is_solved = all(len(values) == 1 for key, values in self.csp.domain.items())
        self.reassign_puzzle()

        return self.is_solved


def get_unassigned_cell(puzzle, domain):

    min_remaining_values = 10

    for row in 'ABCDEFGHI':
        for column in '123456789':
            if puzzle[row + column] == 0:
                possible_values = domain[row + column]

                if len(possible_values) < min_remaining_values:
                    min_remaining_values = len(possible_values)
                    unassigned_cell = row + column

    return unassigned_cell


def consistent(puzzle, cell_constraints, unassigned_cell=None, possible_cell_value=1):
    return all(not (possible_cell_value == puzzle[constraint[1]]) for constraint in cell_constraints)


def forward_check(new_puzzle, cell_constraints, new_domain, unassigned_cell, possible_value):

    for constraint in cell_constraints:
        check_key = constraint[1]

        if new_puzzle[check_key] == 0:

            if possible_value in new_domain[check_key]:
                new_domain[check_key].remove(possible_value)

            if not new_domain[check_key]:

                return False, new_puzzle, new_domain

    return True, new_puzzle, new_domain


def solve_using_backtracking(puzzle, cell_constraints_map, domain):

    if all(value > 0 for key, value in puzzle.items()):
        return True, puzzle, domain

    unassigned_cell = get_unassigned_cell(puzzle, domain)

    for val in domain[unassigned_cell]:

        if consistent(puzzle, cell_constraints_map[unassigned_cell], unassigned_cell, val):
            new_puzzle = deepcopy(puzzle)
            new_domain = deepcopy(domain)
            new_puzzle[unassigned_cell] = val
            new_domain[unassigned_cell] = [val]
            forward_check_result, \
            new_puzzle, \
            new_domain = forward_check(new_puzzle,
                                       cell_constraints_map[unassigned_cell],
                                       new_domain, unassigned_cell, val)

            if forward_check_result == True:
                # TODO: Replace recursive call with Stack using collections.deque
                solved, \
                new_puzzle, \
                new_domain = solve_using_backtracking(new_puzzle,
                                                      cell_constraints_map,
                                                      new_domain)

                if solved:
                    return True, new_puzzle, new_domain

    return False, puzzle, domain


class SudokuCSP:
    __slots__ = ('puzzle', 'all_cells', 'constraints', 'domain',
                 'binary_constraints', 'unassigned_cells',
                 'cell_to_constraint')

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.all_cells = puzzle.all_cells()
        self.constraints = self._gen_constraints()
        self.unassigned_cells = puzzle.get_unassigned_cells()
        self.domain = self._gen_domain()
        self.cell_to_constraint = defaultdict(list)
        self.binary_constraints = []
        self._gen_binary_constraints()

    def _gen_domain(self):

        domain = defaultdict(list)
        all_possible_values = [val for val in range(1, 10)]

        for cell in self.all_cells:
            cell_value = self.puzzle.get_cell(cell)

            if cell_value != 0:
                domain[cell] = [cell_value]

            else:
                domain[cell] = deepcopy(all_possible_values)

        return domain


    def _gen_constraints(self):

        columns = '123456789'
        rows = 'ABCDEFGHI'

        row_constraints = [
            [row + col for col in columns] for row in rows
        ]

        column_constraints = [
            [row + col for row in rows] for col in columns
        ]

        square_constraints = [
            ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"],
            ["D1", "D2", "D3", "E1", "E2", "E3", "F1", "F2", "F3"],
            ["G1", "G2", "G3", "H1", "H2", "H3", "I1", "I2", "I3"],
            ["A4", "A5", "A6", "B4", "B5", "B6", "C4", "C5", "C6"],
            ["D4", "D5", "D6", "E4", "E5", "E6", "F4", "F5", "F6"],
            ["G4", "G5", "G6", "H4", "H5", "H6", "I4", "I5", "I6"],
            ["A7", "A8", "A9", "B7", "B8", "B9", "C7", "C8", "C9"],
            ["D7", "D8", "D9", "E7", "E8", "E9", "F7", "F8", "F9"],
            ["G7", "G8", "G9", "H7", "H8", "H9", "I7", "I8", "I9"]
        ]

        constraints = []

        for constraints_list in [row_constraints, column_constraints, square_constraints]:

            for constraint in constraints_list:
                constraints.append(constraint)

        return constraints

    def _add_to_binary_constraints(self, cell):
        filtered_constraints = filter(lambda c: cell in c, self.constraints)

        for constraint in filtered_constraints:

            for _cell in constraint:

                if _cell != cell:
                    self.binary_constraints.append((cell, _cell))

    def _gen_binary_constraints(self):

        for cell in self.all_cells:
            self._add_to_binary_constraints(cell)

        self.binary_constraints = list(set(self.binary_constraints))

        for constraint in self.binary_constraints:
            self.cell_to_constraint[constraint[0]].append(constraint)

    def get_neighbor_cells(self, X=None, restriction=None):
        neighbors = []
        filtered_arcs = filter(lambda arc: X == arc[0], self.binary_constraints)

        for fa in filtered_arcs:

            if restriction and restriction != fa[1]:
                neighbors.append(fa[1])

            else:
                neighbors.append(fa[1])

        return neighbors

    def get_unassigned_cells(self):

        return self.unassigned_cells
