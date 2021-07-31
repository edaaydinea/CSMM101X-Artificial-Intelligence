Week 4 Project: Adversarial Search and Games
============================================
### **INSTRUCTIONS**

In this assignment you will create an agent to intelligently play the **2048-puzzle** game, using more advanced techniques to probe the search space than the simple methods used in the previous assignment. If you have not played the game before, you may do so at **[gabrielecirulli.github.io/2048](http://gabrielecirulli.github.io/2048)** to get a sense of how the game works. You will implement an adversarial search algorithm that plays the game intelligently, perhaps much more so than playing by hand.

Please read all sections of the instructions carefully.

**I.** Introduction
**II.** Algorithm Review
**III.** Using The Skeleton Code
**IV.** What You Need To Submit
**V.** Important Information
**VI.** Before You Submit

**Bonus Points:**

****Submitting project 2 before 11/01/2020, 23:30 UTC is eligible for bonus points (we count grades on your latest submission). Due to edX policy, all assignment grades are capped at 100%.****

**The assignment's final due date is 12/13/2020, 23:30 UTC.**

### **I. Introduction**

An instance of the 2048-puzzle game is played on a **4×4 grid**, with numbered tiles that slide in all four directions when a player moves them. Every turn, a new tile will randomly appear in an empty spot on the board, with a value of either 2 or 4. Per the input direction given by the player, all tiles on the grid slide as far as possible in that direction, until they either (1) collide with another tile, or (2) collide with the edge of the grid. If two tiles of the same number collide while moving, they will merge into a single tile, valued at the sum of the two original tiles that collided. The resulting tile cannot merge with another tile again in the same move.

![](https://studio.edx.org/asset-v1:ColumbiaX+CSMM.101x+1T2017+type@asset+block@p2_1.png) ![](https://studio.edx.org/asset-v1:ColumbiaX+CSMM.101x+1T2017+type@asset+block@p2_3.png) ![](https://studio.edx.org/asset-v1:ColumbiaX+CSMM.101x+1T2017+type@asset+block@p2_2.png)

In the first assignment, you had ample experience with the process of abstracting ideas and designing functions, classes, and data structures. The goal was to get familiar with how objects, states, nodes, functions, and implicit or explicit search trees are implemented and interact in practice. This time, the focus is strictly on the ground-level details of the algorithms. You will be provided with all the **skeleton code** necessary to get started, so that you can focus solely on optimizing your algorithm.

With typical board games like chess, the two players in the game (i.e. the "Computer AI" and the "Player") take similar actions in their turn, and have similar objectives to achieve in the game. In the 2048-puzzle game, the setup is inherently **asymmetric**; that is, the computer and player take drastically different actions in their turns. Specifically, the computer is responsible for placing random tiles of 2 or 4 on the board, while the player is responsible for moving the pieces. However, adversarial search can be applied to this game just the same.

### **II. Algorithm Review**

Before you begin, review the lecture slides on **adversarial search**. Is this a zero-sum game? What is the minimax principle? In the 2048-puzzle game, the computer AI is technically not "adversarial". In particular, all it does is spawn random tiles of 2 and 4 each turn, with a designated probability of either a 2 or a 4; it certainly does not specifically spawn tiles at the most inopportune locations to foil the player's progress. However, we will create a "Player AI" to play **as if** the computer is completely adversarial. In particular, we will employ the **minimax algorithm** in this assignment.

Remember, in game-playing we generally pick a **strategy** to employ. With the minimax algorithm, the strategy assumes that the computer opponent is perfect in minimizing the player's outcome. Whether or not the opponent is actually perfect in doing so is another question. As a general principle, how far the actual opponent's actual behavior deviates from the assumption certainly affects how well the AI performs [**1**]. However, you will see that this strategy works well in this game. In this assignment, we will implement and optimize the minimax algorithm.

.

![](https://studio.edx.org/asset-v1:ColumbiaX+CSMM.101x+1T2017+type@asset+block@mm4.png)

[**1**] As we saw in the case of a simple game of tic-tac-toe, it is useful to employ the minimax algorithm, which assumes that the opponent is a perfect "minimizing" agent. In practice, however, we may encounter a **sub-par opponent** that makes silly moves. When this happens, the algorithm's assumption deviates from the actual opponent's behavior. In this case, it still leads to the desired outcome of never losing. However, if the deviation goes the other way (e.g. suppose we employ a "maximax" algorithm that assumes that the opponent wants us to win), then the outcome would certainly be different.

### **III. Using The Skeleton Code**

To let you focus on the details of the algorithm, a skeleton code is provided to help you get started, and to allow you to test your algorithm on your own. The skeleton code includes the following files. Note that you will only be working in **one** of them, and the rest of them are read-only:

  -   **Read-only**: GameManager.py. This is the driver program that loads your Computer AI and Player AI, and begins a game where they compete with each other. See below on how to execute this program.

  -   **Read-only**: Grid.py. This module defines the Grid object, along with some useful operations: move(), getAvailableCells(), insertTile(), and clone(), which you may use in your code. These are available to get you started, but they are by no means the most efficient methods available. If you wish to strive for better performance, feel free to ignore these and write your own helper methods in a separate file.

  -   **Read-only**: BaseAI.py. This is the base class for any AI component. All AIs inherit from this module, and implement the getMove() function, which takes a Grid object as parameter and returns a move (there are different "moves" for different AIs).

  -   **Read-only**: ComputerAI.py. This inherits from BaseAI. The getMove() function returns a computer action that is a tuple (x, y) indicating the place you want to place a tile.

  -   **Writable**:PlayerAI.py. You will create this file, and this is where you will be doing your work. This should inherit from BaseAI. The getMove() function, which you will need to implement, returns a number that indicates the player's action. In particular, 0 stands for "Up", 1 stands for "Down", 2 stands for "Left", and 3 stands for "Right". You need to create this file and make it as intelligent as possible. You may include other files in your submission, but they will have to be included through this file.

  -   **Read-only**: BaseDisplayer.py and Displayer.py. These print the grid.

To test your code, execute the game manager like so:

    $ python3 GameManager.py

The progress of the game will be displayed on your terminal screen, with one snapshot printed after each move that the Computer AI or Player AI makes. The Player AI is allowed **0.2 seconds** to come up with each move. The process continues until the game is over; that is, until no further legal moves can be made. At the end of the game, the **maximum tile value** on the board is printed.

**IMPORTANT**: Do not modify the files that are specified as read-only. When your submission is graded, the grader will first automatically **over-write** all read-only files in the directory before executing your code. This is to ensure that all students are using the same game-play mechanism and computer opponent, and that you cannot "work around" the skeleton program and manually output a high score.

### **IV. What You Need To Submit**

Your job in this assignment is to write PlayerAI.py, which intelligently plays the 2048-puzzle game. Here is a snippet of **starter code** to allow you to observe how the game looks when it is played out. In the following "naive" Player AI. The getMove() function simply selects a next move in random out of the available moves:

    from random import randint
    from BaseAI import BaseAI
    
    class PlayerAI(BaseAI):
      def getMove(self, grid):
        moves = grid.getAvailableMoves()
        return moves[randint(0, len(moves) - 1)] if moves else None

Of course, that is indeed a very naive way to play the 2048-puzzle game. If you submit this as your finished product, you will likely receive a grade of zero. You should implement your Player AI with the following points in mind:

  -   Employ the **minimax algorithm**. This is a requirement. There are many viable strategies to beat the 2048-puzzle game, but in this assignment we will be practicing with the minimax algorithm.

  -   Implement **alpha-beta pruning**. This is a requirement. This should speed up the search process by eliminating irrelevant branches. In this case, is there anything we can do about move ordering?

  -   Use **heuristic functions**. What is the maximum height of the game tree? Unlike elementary games like tic-tac-toe, in this game it is highly impracticable to search the entire depth of the theoretical game tree. To be able to cut off your search at any point, you must employ **heuristic functions** to allow you to assign approximate values to nodes in the tree. Remember, the time limit allowed for each move is 0.2 seconds, so you must implement a systematic way to cut off your search before time runs out.

  -   Assign **heuristic weights**. You will likely want to include more than one heuristic function. In that case, you will need to assign weights associated with each individual heuristic. Deciding on an appropriate set of weights will take careful reasoning, along with careful experimentation. If you feel adventurous, you can also simply write an optimization meta-algorithm to iterate over the space of weight vectors, until you arrive at results that you are happy enough with.

### **V. Important Information**

Please read the following information carefully. Before you post a clarifying question on the discussion board, make sure that your question is not already answered in the following sections.

**1\. Note on Python 3**

  The current version of **Python is 3.6.4.   **

**2\. Basic Requirements**

Your submission **must** fulfill the following requirements:

-   You must use adversarial search in your PlayerAI (minimax with alpha-beta pruning).
-   You must provide your move within the time limit of 0.2 seconds.
-   You must name your file PlayerAI.py.
-   Your grade will depend on the maximum tile values your program usually gets to.

**3\. Grading Submissions**

Grading is exceptionally straightforward for this project:** the better your Player AI performs, the higher your grade. **While this is straightforward, we admit that this Adversarial Search project is the most difficult project in this class because of its open-endedness. Your Player AI will be pitted against the standard Computer AI for a total of** 10 games**, and the **maximum tile value** of each game will be recorded. Among the 10 runs, we pick and average **top 5** maximum tile values. Based on the average of these 5 maximum tile values, your submission will be assessed out of a total of **100 points**.

  -   Submissions that are no better than **random** will receive a score of zero.

  -   **Submissions which contains two 1024 runs and three 2048 runs will ****receive full credit.** For example, [256, 512, 512, 512, 1024, 1024, 1024, 2048, 2048, 2048] will receive full credit.

  -   Submissions that fall somewhere in between will receive partial credit on a **logarithmic** scale. That is, every time you manage to double your average maximum tile value, you will be moving your final grade up in equally-spaced notches (instead of doubling as well). For other credit examples, please see Week 4 Project FAQs.
