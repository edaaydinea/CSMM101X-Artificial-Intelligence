"""
In this project, Skeleton code of Project 1 of Columbia University's AI EdX course is used.(8-puzzle).
Python 3
"""

# Importing necessary libraries
import queue as q
import time
import sys
import math
import heapq
import os
import psutil


# SKELETON CODE

# The Class that Represents the Puzzle

class PuzzleState(object):
    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        if n * n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []

        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break

    def append_action(self, action):
        self.action = "{}{}".format(action, self.action)

    def get_action(self):
        return self.action

    def get_config(self):
        return self.config

    def get_cost(self):
        return self.cost

    def get_parent(self):
        return self.parent

    def get_path(self):
        action_list = []
        parent = self
        for i in range(self.get_cost() - 1):
            action_list.append(parent.get_action())
            parent = parent.get_parent()
        return action_list[::-1]

    def display(self):

        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)

    def move_left(self):

        if self.blank_col == 0:
            return None

        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:
            return None

        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:
            return None

        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:
            return None

        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:
            up_child = self.move_up()

            if up_child is not None:
                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:
                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:
                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:
                self.children.append(right_child)

        return self.children


def mapping(state):
    map = {'Up': 0,
           'Down': 1,
           'Left': 2,
           'Right': 3}

    return map[state.get_action()]


# Function that Writes to output.txt

# Students need to change the method to have the corresponding parameters

def writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth, running_time, max_ram_usage):
    # In this section, I will create the 'output.txt' to write all result.

    with open("output.txt", "w") as file:
        file.write("path_to_goal: {}\n".format(path_to_goal))
        file.write("cost_of_path: {}\n".format(cost_of_path))
        file.write("nodes_expanded: {}\n".format(nodes_expanded))
        file.write("search_depth: {}\n".format(search_depth))
        file.write("running_time: {}\n".format(running_time))
        file.write("max_ram_usage: {}\n".format(max_ram_usage))


def output_formating(state):
    action_list = [state.get_action()]
    parent = state.get_parent()

    for i in range(state.get_cost() - 1):
        action_list.append(parent.get_action())
        parent = parent.get_parent()
    return action_list[::-1], state.get_cost()


def bfs_search(initial_state):
    """BFS search"""

    # First, I will determine the basic variables such as frontier, explored,  path  for bfs search.

    time_bfs_1 = time.time()
    # construction of a FIFO( First in First Out) queue
    frontier = q.Queue()
    # Put the initial state into the queue
    frontier.put(initial_state)
    # Create unordered and unindexed collection
    explored = set()
    frontier_set = set()
    frontier_set.add(initial_state.get_config())
    current_depth = 0

    while not frontier.empty():
        state = frontier.get()

        if test_goal(state):
            time_bfs_2 = time.time()
            process = psutil.Process(os.getpid())
            path_to_goal, cost_of_path = output_formating(state)

            return writeOutput(path_to_goal, cost_of_path, len(explored), current_depth, time_bfs_2 * time_bfs_1,
                               process.memory_info().rss)

        frontier_set.remove(state.get_config())
        explored.add(state.get_config())
        neighbors = state.expand()

        for neighbor in neighbors:
            if neighbor.get_config() not in explored and neighbor.get_config() not in frontier_set:
                frontier.put(neighbor)
                frontier_set.add(neighbor.get_config())
                if neighbor.get_cost() > current_depth:
                    current_depth = neighbor.get_cost()


def dfs_search(initial_state):
    """DFS search"""

    time_dfs_1 = time.time()
    frontier = [initial_state]
    frontier_set = set()
    frontier_set.add(initial_state.get_config())
    explored = set()
    current_depth = 0

    while len(frontier) > 0:
        state = frontier.pop()
        frontier_set.remove(state.get_config())

        if test_goal(state):
            time_dfs_2 = time.time()
            process = psutil.Process(os.getpid())
            path_to_goal, cost_of_path = output_formating(state)

            return writeOutput(path_to_goal, cost_of_path, len(explored), current_depth, time_dfs_2 - time_dfs_1,
                               process.memory_info().rss)

        explored.add(state.get_config())
        neighbors = state.expand()[::-1]

        for neighbor in neighbors:
            if neighbor.get_config() not in explored and neighbor.get_config() not in frontier_set:
                frontier.append(neighbor)
                frontier_set.add(neighbor.get_config())
                if neighbor.get_cost() > current_depth:
                    current_depth = neighbor.get_cost()


def A_star_search(initial_state):
    """A * search"""

    time_star_1 = time.time()
    frontier_set = set()
    frontier_set.add(initial_state.get_config())
    explored = set()
    current_depth = 0

    entry = 0
    frontier_heap = []
    heapq.heappush(frontier_heap, (0, entry, initial_state))

    while len(frontier_heap) > 0:
        state = heapq.heappop(frontier_heap)
        frontier_set.remove(state[2].get_config())

        if test_goal(state[2]):
            time_star_2 = time.time()
            process = psutil.Process(os.getpid())
            path_to_goal, cost_of_path = output_formating(state)

            return writeOutput(path_to_goal, cost_of_path, len(explored), current_depth, time_star_2 - time_star_1,
                               process.memory_info().rss)

        explored.add(state[2].get_config())
        neighbors = state[2].expand()[::-1]

        for neighbor in neighbors:
            entry += 1
            if neighbor.get_config() not in explored and neighbor.get_config() not in frontier_set:
                distance = calculate_total_cost(neighbor)
                heapq.heappush(frontier_heap, (distance, entry, neighbor))
                frontier_set.add(neighbor.get_config())
                if neighbor.get_cost() > current_depth:
                    current_depth = neighbor.get_cost()


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""

    return calculate_manhattan_dist(state) + state.get_cost()


def calculate_manhattan_dist(state):
    """calculate the manhattan distance of a tile"""

    config = state.get_config()
    total_distance = 0

    for i in range(1, 9):
        total_distance = total_distance + (abs(i // 3 - config.index(i) // 3) + abs(i % 3 - config.index(i) % 3))
    return total_distance


def test_goal(puzzle_state):
    """test the state is the goal state or not"""

    goal_config = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    if puzzle_state.get_config() == goal_config:
        return True
    return False


# Main Function that reads in Input and Runs corresponding Algorithm

def main():
    """if len(sys.argv) < 3:
        print()
        exit(1)"""

    sm = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)

    if sm == "bfs":
        bfs_search(hard_state)

    elif sm == "dfs":
        dfs_search(hard_state)

    elif sm == "ast":
        A_star_search(hard_state)

    else:

        print("Enter valid command arguments !")


if __name__ == '__main__':
    main()
