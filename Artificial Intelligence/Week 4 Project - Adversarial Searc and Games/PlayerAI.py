"""
 Columbia CSMM.101x Artificial Intelligence Week 4 - Project 2

 This should inherit from BaseAI. The getMove() function, which I will need to
 implement, returns a number that indicates the player’s action.

 {
    0: "Up",
    1: "Down",
    2: "Left",
    3: "Right"
 }

"""

# Import necessary libraries

from itertools import chain
from BaseAI import BaseAI


class PlayerAI(BaseAI):
    __slots__ = ('tiles', 'max_depth')

    def __init__(self):
        self.tiles = [2, 4]
        self.max_depth = 4

    def terminal_test(self, grid=None):
        return not grid.canMove() or self.max_depth <= grid.depth

    def maximize_algorithm(self, grid=None, alpha=float('-Inf'), beta=float('Inf)')):
        if self.terminal_test(grid):
            return None, self.eval_function(grid)

        (max_child, max_utility) = (None, float('-Inf'))
        children = grid.getAvailableMoves()

        for child in children:
            grid = grid.clone()
            grid.depth = grid.depth + 1
            grid.move(child)
            (_, utility) = self._minimize(grid, alpha=alpha, beta=beta)

            if utility > max_utility:
                (max_child, max_utility) = (child, utility)

            if beta <= max_utility:
                break

        return max_child, max_utility

    def minimize_algorithm(self, grid, alpha=float('-Inf'), beta=float('Inf)')):

        if self.terminal_test(grid):
            return None, self.eval_function(grid)

        (min_child, min_utility) = (None, float('Inf'))
        children = grid.getAvailableCells()

        for tile in self.tiles:
            for child in children:
                grid = grid.clone()
                grid.depth = grid.depth + 1
                grid.insertTile(child, tile)

                (_, utility) = self.maximize(grid, alpha=alpha, beta=beta)

                if utility < min_utility:
                    (min_child, min_utility) = (grid, utility)

                if min_utility <= alpha:
                    break

                beta = min(min_utility, beta)

        return min_child, min_utility

    @staticmethod
    def heuristic_function(grid=None):

        heuristic1 = len(grid.getAvailableCells()) / (grid.size ** 2)
        penalty = 0
        total_sum = sum(chain.from_iterable(grid.map))

        for i in range(grid.size):
            for j in range(i, grid.size - 1):
                penalty = penalty + abs(grid.map[i][j + 1] - grid.map[i][j])

        for i in range(grid.size):
            for j in range(i, grid.size - 1):
                penalty = penalty + abs(grid.map[j][i + 1] - grid.map[j][i])

        heuristic2 = penalty / (2 * total_sum)

        return heuristic1 - heuristic2

    def getMove(self, grid=None):
        grid.depth = 0
        (move, _) = self.maximize(grid, alpha=float('-Inf'), beta=float("Inf"))

        return move
