"""
CSMM.101X - Columbia University - Artificial Intelligence - Week 7 Project 3 - Classification
"""

# Import necessary libraries
import sys
from os.path import exists
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split


class Classification:
    __slots__ = ("X", "y", "data", "train_X", "train_y", "test_X", "test_y")


    def __init__(self, csv_file_path=None, target_column=None):
        self.X = None
        self.y = None
        self.data = None
        self.train_X = None
        self.train_y = None
        self.test_X = None
        self.test_X = None
        self.test_y = None

        self.load_data(csv_file=csv_file_path, target_column=target_column, column_headers=["A", "B", "label"])

    def load_data(self, csv_file=None, target_column=None, column_headers=None):

        if not isinstance(csv_file, str):
            raise TypeError(f"{csv_file} should be {str}")

        if target_column is not None and not isinstance(target_column, str):
            raise TypeError(f"{target_column} should be {str}")

        if not exists(csv_file):
            raise IOError(f"{csv_file} file path does not exist")

        self.data = pd.read_csv(csv_file, header=column_headers if not column_headers else 0)

        # Setting the last column as target column
        if target_column is None:
            target_column = self.data.columns[len(self.data.columns) - 1]

        # Setting X and y by using dataset, and target column
        self.y = self.data[target_column]
        self.data.drop(columns=[target_column], inplace=True)  # The dataset changed here.
        self.X = self.data  # The X dataset doesn't include target column.

        # Train - Test Splitting
        self.train_X, self.test_X, self.train_y, self.test_y = train_test_split(self.X, self.y,
                                                                                test_size=0.4,
                                                                                random_state=42,
                                                                                stratify=self.y)

    global scoring
    scoring = "f1_score"

    def get_best_model_and_accuracy(self, model_prefix=None, model=None, scoring=scoring, **kwargs):
        grid = GridSearchCV(model, param_grid=kwargs.get("kwargs"), cv=5, scoring=scoring, n_jobs=-1)
        grid.fit(X=self.train_X, y=self.train_y)

        # Evaluating Predictions on Test Data
        test_score = grid.score(self.test_X, self.test_y)

        return model_prefix, grid.best_score_, test_score


    def support_vector_machine_linear(self, model_prefix="svm_linear", scoring=scoring, **kwargs):
        svm_linear = SVC()

        return self.get_best_model_and_accuracy(model_prefix=model_prefix,
                                                model=svm_linear,
                                                scoring=scoring,
                                                kwargs=kwargs)

    def support_vector_machine_polynomial(self, model_prefix='svm_polynomial', scoring=scoring, **kwargs):
        svm_poly = SVC()
        return self.get_best_model_and_accuracy(model_prefix=model_prefix,
                                                model=svm_poly,
                                                scoring=scoring,
                                                kwargs=kwargs)

    def support_vector_machine_rbf(self, model_prefix='svm_rbf', scoring=scoring, **kwargs):
        svm_rbf = SVC()
        return self.get_best_model_and_accuracy(model_prefix=model_prefix,
                                                model=svm_rbf,
                                                scoring=scoring,
                                                kwargs=kwargs)

    def logistic_regression(self, model_prefix='logistic', scoring=scoring, **kwargs):
        logistic_regression = LogisticRegression()
        return self.get_best_model_and_accuracy(model_prefix=model_prefix,
                                                model=logistic_regression,
                                                scoring=scoring,
                                                kwargs=kwargs)

    def knn(self, model_prefix='knn', scoring=scoring, **kwargs):
        knn = KNeighborsClassifier()
        return self.get_best_model_and_accuracy(model_prefix=model_prefix,
                                                model=knn,
                                                scoring=scoring,
                                                kwargs=kwargs)

    def decision_tree(self, model_prefix='decision_tree', scoring=scoring, **kwargs):
        decision_tree = DecisionTreeClassifier()
        return self.get_best_model_and_accuracy(model_prefix=model_prefix,
                                                model=decision_tree,
                                                scoring=scoring,
                                                kwargs=kwargs)

    def random_forest(self, model_prefix='random_forest', scoring=scoring, **kwargs):
        random_forest = RandomForestClassifier()
        return self.get_best_model_and_accuracy(model_prefix=model_prefix,
                                                model=random_forest,
                                                scoring=scoring,
                                                kwargs=kwargs)

    def train_model(self, output_csv_file='output.csv'):
        classifier_scores = []

        def change_to_csv_row(x):
            return ','.join(map(str, x))

        classifier_scores.append(change_to_csv_row(self.support_vector_machine_linear(scoring='accuracy',
                                                                                      C=[0.1, 0.5, 1, 5, 10, 50, 100],
                                                                                      kernel=('linear',))))
        classifier_scores.append(change_to_csv_row(self.support_vector_machine_polynomial(scoring='accuracy',
                                                                                          C=[0.1, 1, 3],
                                                                                          degree=[4, 5, 6],
                                                                                          gamma=[0.1, 0.5],
                                                                                          kernel=('poly',))))
        classifier_scores.append(change_to_csv_row(self.support_vector_machine_rbf(scoring='accuracy',
                                                                                   C=[0.1, 0.5, 1, 5, 10, 50, 100],
                                                                                   gamma=[0.1, 0.5, 1, 3, 6, 10],
                                                                                   kernel=('rbf',))))
        classifier_scores.append(change_to_csv_row(self.logistic_regression(scoring='accuracy',
                                                                            C=[0.1, 0.5, 1, 5, 10, 50, 100])))
        classifier_scores.append(change_to_csv_row(self.knn(scoring='accuracy',
                                                            n_neighbors=[val for val in range(1, 51)],
                                                            leaf_size=[val for val in range(5, 65, 5)])))
        classifier_scores.append(change_to_csv_row(self.decision_tree(scoring='accuracy',
                                                                      max_depth=[val for val in range(1, 51)],
                                                                      min_samples_split=[val for val in range(2, 11)])))
        classifier_scores.append(change_to_csv_row(self.random_forest(scoring='accuracy',
                                                                      max_depth=[val for val in range(1, 51)],
                                                                      min_samples_split=[val for val in range(2, 11)])))
        # print(classifier_scores)

        if output_csv_file is not None:
            try:
                with open(output_csv_file, 'w') as output_csv:
                    output_csv.writelines(row + '\n' for row in classifier_scores)
            except Exception as e:
                print(e)


def main():
    if len(sys.argv) >= 3:
        pass
    else:
        print("python3 problem3.py input3.csv output3.csv")
        sys.exit(1)

    input_csv_file = str(sys.argv[1])
    output_csv_file = str(sys.argv[2])

    classification = Classification(csv_file_path=input_csv_file)
    classification.train_model(output_csv_file=output_csv_file, target_column="label")


if __name__ == '__main__':
    main()
