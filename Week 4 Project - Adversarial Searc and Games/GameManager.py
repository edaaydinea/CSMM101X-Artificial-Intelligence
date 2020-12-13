"""
This is the driver program that loads the Computer AI and Player AI, and begins
a game where they complete with each other.
"""

# Import necessary libraries
from Grid import Grid
from ComputerAI import ComputerAI
from PlayerAI import PlayerAI
from Displayer import Displayer
from random import randint
import time

default_Initial_Tiles = 2
default_Probability = 0.9

Player_Action_Dic = {
    0: "Up",
    1: "Down",
    2: "Left",
    3: "Right"
}

(Player_Turn, Computer_Turn) = (0, 1)

timeLimit = 0.2
allowance = 0.05


class GameManager:

    def __init__(self, size=4):
        self.previousTime = time.clock()
        self.possibleNewTiles = None
        self.grid = Grid(size)
        self.possible_New_Tiles = [2, 4]
        self.probability = default_Probability
        self.initTiles = default_Initial_Tiles
        self.computerAI = None
        self.playerAI = None
        self.displayer = None
        self.over = False

    def setComputer(self, computerAI):
        self.computerAI = computerAI

    def setPlayerAI(self, playerAI):
        self.playerAI = playerAI

    def setDisplayer(self, displayer):
        self.displayer = displayer

    def UpdateAlarm(self, currentTime):
        if currentTime - self.previousTime > timeLimit + allowance:
            self.over = True
        else:
            while time.clock() - self.previousTime < timeLimit + allowance:
                pass

            self.previousTime = time.clock()

    def start(self):
        for i in range(self.initTiles):
            self.insertRandonTile()

        self.displayer.display(self.grid)

        turn = Player_Turn
        maxTile = 0

        while not self.isGameOver() and not self.over:
            gridCopy = self.grid.clone()

            if turn == Player_Turn:
                print("Player's Turn:", end="")
                move = self.playerAI.getMove(gridCopy)
                print(Player_Action_Dic[move])

                if move is not None and 0 <= move < 4:

                    if self.grid.canMove([move]):
                        self.grid.Move(move)
                        maxTile = self.grid.getMaxTile()

                    else:
                        print("Invalid PlayerAI Move")
                        self.over = True

                else:
                    print("Invalid PlayerAI Move -1")
                    self.over = True

            else:
                print("Computer's Turn:")
                move = self.computerAI.getMove(gridCopy)

                if move and self.grid.canInsert(move):
                    self.grid.setCellValue(move, self.getNewTileValue())
                else:
                    print("Invalid Computer AI Move")
                    self.over = True

                if not self.over:
                    self.displayer.display(self.grid)

                    # Exceeding the Time Allotted for Any Turn Terminates the Game
                self.UpdateAlarm(time.clock())

                turn = 1 - turn
            print(maxTile)

    def isGameOver(self):
        return not self.grid.canMove()

    def getNewTileValue(self):
        if randint(0, 99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1]

    def insertRandonTile(self):
        tileValue = self.getNewTileValue()
        cells = self.grid.getAvailableCells()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.setCellValue(cell, tileValue)

    @staticmethod
    def main():
        gameManager = GameManager()
        playerAI = PlayerAI()
        computerAI = ComputerAI()
        displayer = Displayer()

        gameManager.setPlayerAI(playerAI)
        gameManager.computerAI(computerAI)
        gameManager.displayer(displayer)

        gameManager.start()

    if __name__ == '__main__':
        main()
