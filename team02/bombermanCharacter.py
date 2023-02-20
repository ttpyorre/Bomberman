# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

# Import Priority Queue
from priorityQueue import PriorityQueue
import numpy as np
import math
import bombState

class BombermanCharacter(CharacterEntity):

    # def do(self, wrld):

    #     neighbors = self.astar(wrld, True)

    #     for n in neighbors:
    #         self.set_cell_color(n[0], n[1], Fore.RED + Back.BLUE)

    WALK_PATH = 0
    AVOID_BOMB = 1

    STATE = 0

    def do(self, wrld):
        # Astar gives us a path of nodes that we visit one by one
        path = self.astar(wrld, True)

        # visual debugging of the path
        for p in path:
            self.set_cell_color(p[0], p[1], Fore.RED + Back.BLUE)

        self.number = self.number + 1
        print(self.number)

        while path:
            walk = path.pop()
            if wrld.wall_at(walk[0], walk[1]):
                print("wall")
                self.place_bomb()
                
                # we also need to get out of the range of the bomb
                corner = self.neighbors_of_4_corners(wrld, self.x, self.y)
                c = corner.pop()
                self.set_cell_color(c[0], c[1], Fore.RED + Back.YELLOW)
                self.move(c[0] - self.x, c[0] - self.y)
            else:
                self.move(walk[0] - self.x, walk[1] - self.y)

    @staticmethod
    def neighbors_of_8(wrld, x, y, ignore_walls = False):
        '''
        Returns walkable neighbor cells of the cell we are currently in.
        :param wrld         [SensedWorld]   world object
        :param x            [int]           x coordinate in world
        :param y            [int]           y coordinate in world
        :param ignore_walls [Bool]          do we ignore walls in out path
        :return             [[(int, int)]]  list of all neighbors that are available
        '''
        # we search with right, down, left, up priority
        neighbors = [(x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y), (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
        availableNeighbors = []

        for neighbor in neighbors:
            if neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < wrld.width() and neighbor[1] < wrld.height():
                if ignore_walls:
                    availableNeighbors.append(neighbor)
                elif wrld.wall_at(neighbor[0], neighbor[1]) != True:
                    availableNeighbors.append(neighbor)

        return availableNeighbors

    @staticmethod
    def neighbors_of_4_corners(wrld, x, y, ignore_walls = False):
        '''
        Returns walkable neighbor cells of the cell we are currently in.
        :param wrld         [SensedWorld]   world object
        :param x            [int]           x coordinate in world
        :param y            [int]           y coordinate in world
        :param ignore_walls [Bool]          do we ignore walls in out path
        :return             [[(int, int)]]  list of all neighbors that are available
        '''
        # we search with right, down, left, up priority
        neighbors = [(x + 1, y + 1), (x - 1, y + 1), (x - 1, y - 1), (x + 1, y - 1)]
        availableNeighbors = []

        for neighbor in neighbors:
            if neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < wrld.width() and neighbor[1] < wrld.height():
                if wrld.wall_at(neighbor[0], neighbor[1]) != True:
                    availableNeighbors.append(neighbor)

        return availableNeighbors

    
                

    @staticmethod
    def heuristics(start, goal):
        '''
        :param start [int, int]
        :param goal  [int, int]
        :return euclidean distance.
        '''
        return math.sqrt(pow(abs(start[0] - goal[0]), 2) + pow(abs(start[1] - goal[1]), 2))

    def astar(self, wrld, ignore_walls = False):
        '''
        :param wrld         [SensedWorld] world object
        :param ignore_walls [Bool] do we ignore walls in out path
        :return path        [[(int, int)]] fastest path from current to goal
        '''
        start = (self.x, self.y)
        goal = wrld.exitcell

        # Establishing our queue
        queue = PriorityQueue()
        queue.put(start, 0)
        
        cameFrom = {}
        cost = {}
        cost_to_visit_node = 1
        cameFrom[start] = None
        cost[start] = 0

        exploredMap = []
        path = []

        while not queue.empty():
            current = queue.get()

            if goal == current: # found goal
                break

            nextNodes = BombermanCharacter.neighbors_of_8(wrld, current[0], current[1], ignore_walls)
            for nextNode in nextNodes:
                new_cost = cost[current] + cost_to_visit_node
                if nextNode not in cost or new_cost < cost[nextNode]:
                    cost[nextNode] = new_cost
                    priority = new_cost + BombermanCharacter.heuristics(nextNode, goal)
                    queue.put(nextNode, priority)
                    cameFrom[nextNode] = current
        
        # We make our path
        while current != start:
            path.insert(0, current)
            current = cameFrom[current]

        return path
