"""
CSMM.101X - Columbia University - Artificial Intelligence - Week 7 Project - SUDOKU
"""
# Import necessary libraries
from driver import test_sudoku_solver
from unittest import TestCase, main


class TestSudoku(TestCase):

    def setUp(self):
        self.inputs = []
        self.outputs = []

        with open('sudokus_start.txt', 'r') as input_file:
            self.inputs = input_file.readlines()

        with open('sudokus_finish.txt', 'r') as output_file:
            self.outputs = output_file.readlines()

    def test_sudoku(self):

        for puzzle, output in zip(self.inputs, self.outputs):
            solved_puzzle_, algorithm = test_sudoku_solver(puzzle)
            _output = ' '.join([solved_puzzle_, algorithm])
            self.assertEqual(_output, output.strip())


if __name__ == "__main__":
    main()