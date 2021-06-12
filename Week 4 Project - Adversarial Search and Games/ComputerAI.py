"""
This inherits from BaseAI. The getMove() function returns a computer action
that is a tuple (x, y) indicating the place you want to place a tile.

"""

# Import necessary libraries
from random import randint
from BaseAI import BaseAI


class ComputerAI(BaseAI):

    @staticmethod
    def getMove(grid):
        cells = grid.getAvailableCells()

        return cells[randint(0, len(cells) - 1)] if cells else None
