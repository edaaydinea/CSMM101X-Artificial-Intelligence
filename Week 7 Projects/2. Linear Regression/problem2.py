"""
CSMM.101X - Columbia University - Artificial Intelligence - Week 7 Project 2 - Linear Regression
"""
# Import necessary libraries
import sys
from os.path import exists
from numpy import ones, zeros
import pandas as pd


class LinearRegression:
    __slots__ = ('weights', 'data', 'X', 'y', 'learning_rates', 'max_iterations')

    def __init__(self, csv_file=None, learning_rates=None, max_iterations=100):
        self.weights = None
        self.data = None
        self.X = None
        self.y = None
        self.learning_rates = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
        self.max_iterations = len(self.learning_rates) * [max_iterations]
        self.load_dataset(csv_file=csv_file)

    def load_dataset(self, csv_file=None, target_column=None, column_headers=None):

        if not isinstance(csv_file, str):
            raise TypeError(f"{csv_file} should be  {str}")

        if target_column is not None and isinstance(target_column, str):
            raise TypeError(f" {target_column} should be {str}")

        if not exists(csv_file):
            raise IOError(f"{csv_file} file path does not exist")

        self.data = pd.read_csv(csv_file, header=column_headers)

        # Setting the last column as target column
        if target_column is None:
            target_column = self.data.columns[len(self.data.columns) - 1]

        # Setting y value as target column
        self.y = self.data[target_column]

        # Dropping the target column from dataset
        self.data.drop(columns=[target_column], inplace=True)  # The data changed here.

        # Adding Bias Column to the Input Data
        column_index = len(self.data.columns)
        self.normalize_data()
        self.data.insert(column_index, column=column_index, value=ones(len(self.data)))
        self.X = self.data

    def normalize_data(self):

        # Mean of Each Column
        mean = self.data.mean(axis=0)
        standard_deviation = self.data.std(axis=0)
        self.data = self.data - mean
        self.data = self.data / standard_deviation

    def train_model(self, output_csv_file='linear_regression_output.csv'):
        d = len(self.data.columns)
        output_vector = []
        n = len(self.X)

        for alpha, iterations in zip(self.learning_rates, self.max_iterations):

            # Initialize the beta to 0
            self.weights = zeros(d)
            for i in range(iterations):
                fx = self.X.dot(self.weights)
                temp1 = fx - self.y
                temp2 = (self.X.T * temp1).sum(axis=1)
                self.weights = self.weights - ((alpha / n) * temp2)

            weights = self.weights.tolist()
            output_vector.append(",".join(map(str, [alpha, iterations, weights[-1], *weights[:-1]])) + "\n")

        if output_csv_file is not None:
            try:
                with open(output_csv_file, "w") as output_csv:
                    output_csv.writelines(output_vector)
            except Exception as e:
                print(e)


def main():
    if len(sys.argv) < 3:
        print("python3 problem2.py input2.csv output2.csv")
        sys.exit(1)

    input_csv = str(sys.argv[1])
    output_csv = str(sys.argv[2])

    linear_regression = LinearRegression(csv_file=input_csv)
    linear_regression.train_model(output_csv_file=output_csv)


if __name__ == "__main__":
    main()
