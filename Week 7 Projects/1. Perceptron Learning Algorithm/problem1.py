"""
CSMM.101X - Columbia University - Artificial Intelligence - Week 7 Project
"""
# Import necessary libraries

import sys
from os.path import exists
from numpy import zeros, ones
import pandas as pd


class PLA:

    __slots__ = ('weights', 'X', 'y')

    def __init__(self, file=None, target_column=None):
        self.weights = None
        self.X = None
        self.y = None
        self._load_data(file, target_column)

    def _load_data(self, file=None, target_column=None):


        if not isinstance(file, str):
            raise TypeError(f"{file} should be {str}")

        if target_column is not None and not isinstance(target_column, str):
            raise TypeError(f"{target_column} should be {str}")

        if not exists(file):
            raise IOError(f"{file} file path does not exist")

        self.X = pd.read_csv(file, header=None)

        # Determining target column by using last column
        if target_column is None:
            target_column = self.X.columns[len(self.X.columns) - 1]

        self.y = self.X[target_column]

        # Dropping Target Column
        self.X.drop(columns=[target_column], inplace=True)

        # Adding Bias Column
        column_index = len(self.X.columns)
        self.X.insert(column_index, column=column_index, value=ones(len(self.X)))

    def train(self, weights_output_file=None):

        if weights_output_file is not None and not isinstance(weights_output_file, str):
            raise TypeError(f"'{weights_output_file}' should be of {str}")

        d = len(self.X.columns)

        # Initialize the weights to all zeros
        self.weights = zeros(d)

        weights_per_iteration = []

        converged = False
        while not converged:
            converged = True
            for x_i, y_i in zip(self.X.values, self.y.values):
                fxi = x_i.dot(self.weights)
                if (fxi * y_i) <= 0:
                    self.weights = self.weights + (y_i * x_i)
                    converged = False
            weights_per_iteration.append(','.join(map(str, self.weights.tolist())) + "\n")

        if weights_output_file is not None:
            try:
                with open(weights_output_file, 'w') as output_csv:
                    output_csv.writelines(weights_per_iteration)
            except Exception as e:
                print(e)
        return self.weights


def main():

    if len(sys.argv) < 3:
        print("Minimum 2 input arguments needed")
        print("python3 problem1.py input.csv output.csv")
        sys.exit(1)

    input_csv_file = str(sys.argv[1])
    output_csv_file = str(sys.argv[2])
    pla = PLA(file=input_csv_file)
    pla.train(weights_output_file=output_csv_file)


if __name__ == '__main__':
    main()
