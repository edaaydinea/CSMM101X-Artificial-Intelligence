"""
CSMM.101X - Columbia University - Artificial Intelligence - Week 7 Project - SUDOKU
"""
# Import necessary libraries
import sys
from sudoku import Sudoku, solve_using_backtracking

def test_sudoku_solver(test_input):
    return solve_puzzle(test_input)

def puzzle_to_string(puzzle):
    ordered_values = []

    for row in 'ABCDEFGHI':
        for column in '123456789':
            ordered_values.append(puzzle[row+column])
    return ''.join(str(val) for val in ordered_values)

def solve_puzzle(puzzle_string):

    puzzle = Sudoku(board_representation = puzzle_string)

    # Solving with AC3 algorithm
    solved = puzzle.solve_with_ac3()
    algorithm = 'AC3'

    if solved:
        solved_puzzle = puzzle.puzzle
        algorithm= 'AC3'

    else:
        cell_constraints_map = puzzle.csp.cell_to_constraint
        solved, \
        solved_puzzle, \
        solved_domain = solve_using_backtracking(puzzle.puzzle,
                                                 cell_constraints_map,
                                                 puzzle.csp.domain)

        algorithm = 'BTS'

    return puzzle_to_string(solved_puzzle), algorithm

def main():
    puzzle_string = str(sys.argv[1]).strip()
    puzzle_output, algorithm = solve_puzzle(puzzle_string)
    # print(puzzle_output, algorithm)

    with open('output.txt', 'w') as output_file:
        output_file.write(' '.join([puzzle_output.strip(), algorithm]))


if __name__ == "__main__":
    main()

