"""
This module defines the some useful operations:
- clone()
- insertTitle()
- setCellValue()
- getAvailableCells()
- getMaximumTile()
- canInsert()
- move()
- moveUpDown()
- moveLeftRight()
- merge()
- canMove()
- getAvailableMoves()
- crossBound()
- getCellValue()
"""

# Import necessary libraries
from copy import deepcopy

directionVectors = (Up_Vector, Down_Vector, Left_Vector, Right_Vector) = ((-1, 0), (1, 0),
                                                                          (0, -1), (0, 1))
vectorIndex = [Up, Down, Left, Right] = range(4)


class Grid:

    def __init__(self, size=4):
        self.size = size
        self.map = [[0] * self.size for i in range(self.size)]

    def clone(self):
        gridCopy = Grid()
        gridCopy.map = deepcopy(self.map)
        gridCopy.size = self.size

        return gridCopy

    def insertTile(self, pos, value):
        self.setCellValue(pos, value)

    def setCellValue(self, pos, value):
        self.map[pos[0]][pos[1]] = value

    def getAvailableCells(self):
        cells = []

        for x in range(self.size):
            for y in range(self.size):
                if self.map[x][y] == 0:
                    cells.append((x, y))

        return cells

    def getMaximumTile(self):
        maximumTile = 0

        for x in range(self.size):
            for y in range(self.size):
                maximumTile = max(maximumTile, self.map[x][y])

        return maximumTile

    def canInsert(self, pos):
        return self.getCellValue(pos) == 0

    def move(self, dir):
        dir = int(dir)

        if dir == Up:
            return self.moveUpDown(False)
        if dir == Down:
            return self.moveUpDown(True)
        if dir == Left:
            return self.moveUpDown(False)
        if dir == Right:
            return self.moveUpDown(True)

    def moveUpDown(self, down):
        r = range(self.size - 1, -1, -1) if down else range(self.size)
        moved = False

        for y in range(self.size):
            cells = []

            for x in r:
                cell = self.map[x][y]

                if cell != 0:
                    cells.append(cell)

            self.merge(cells)

            for x in r:
                value = cells.pop(0) if cells else 0

                if self.map[x][y] != value:
                    moved = True

                self.map[x][y] = value

        return moved

    def moveLeftRight(self, right):
        r = range(self.size - 1, -1, -1) if right else range(self.size)
        moved = False

        for x in range(self.size):
            cells = []

            for y in r:
                cell = self.map[x][y]

                if cell != 0:
                    cells.append(cell)

            self.merge(cells)

            for y in r:
                value = cells.pop(0) if cells else 0

                if self.map[x][y] != value:
                    moved = True

                self.map[x][y] = value

        return moved

    @staticmethod
    def merge(cells):

        if len(cells) <= 1:
            return cells

        i = 0

        while i < len(cells) - 1:
            if cells[i] == cells[i + 1]:
                cells[i] = cells[i] * 2

                del cells[i + 1]

            i = i + 1

    def canMove(self, dirs=vectorIndex):

        checkingMoves = set(dirs)

        for x in range(self.size):
            for y in range(self.size):

                if self.map[x][y]:

                    for i in checkingMoves:
                        move = directionVectors[i]

                        adjCellValue = self.getCellValue((x + move[0],
                                                          y + move[1]))

                        if adjCellValue == self.map[x][y] or adjCellValue == 0:
                            return True

                elif self.map[x][y] == 0:
                    return True

        return False

    def getAvailableMoves(self, dirs=vectorIndex):

        availableMoves = []

        for i in dirs:
            gridCopy = self.clone()

            if gridCopy.move(i):
                availableMoves.append(i)

        return availableMoves

    def CrossBound(self, pos):

        return pos[0] < 0 or pos[0] >= self.size or pos[1] or pos[1] >= self.size

    def getCellValue(self, pos):

        if not self.CrossBound(pos):
            return self.map[pos[0]][pos[1]]
        else:
            return None


if __name__ == '__main__':
    grid = Grid()
    grid.map[0][0] = 2
    grid.map[1][0] = 2
    grid.map[3][0] = 4

    while True:
        for i in grid.map:
            print(i)

        print(grid.getAvailableMoves())

        input1 = input()
        grid.move(input1)
