# Basic functions we might call for a lot
import sys
sys.path.insert(0, '../bomberman')

from colorama import Fore, Back

# get PriorityQueue
from priorityQueue import PriorityQueue
from entity import CharacterEntity
import numpy as np
import math

def neighbors_of_4(character, wrld, x, y):
    '''
    Returns walkable neighbor cells of the cell we are currently in.
    :param character [CharacterEntity] character object
    :param wrld      [SensedWorld]     world object
    :param x         [int]             x coordinate in world
    :param y         [int]             y coordinate in world
    :return          [[(int, int)]]    list of all neighbors that are available
    '''
    # we search with right, down, left, up priority
    neighbors = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
    availableNeighbors = []

    for neighbor in neighbors:
        if neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < wrld.width() and neighbor[1] < wrld.height():
            if wrld.wall_at(neighbor[0], neighbor[1]) != True:
                availableNeighbors.append(neighbor)

    return availableNeighbors
            

def heuristics(start, goal):
    '''
    :param start [int, int]
    :param goal  [int, int]
    :return euclidean distance.
    '''
    return math.sqrt(pow(abs(start[0] - goal[0]), 2) + pow(abs(start[1] - goal[1]), 2))


def neighbors_of_8(character, wrld, x, y):
    '''
    Returns walkable neighbor cells of the cell we are currently in.
    :param character [CharacterEntity] character object
    :param wrld      [SensedWorld]     world object
    :param x         [int]             x coordinate in world
    :param y         [int]             y coordinate in world
    :return          [[(int, int)]]    list of all neighbors that are available
    '''
    # we search with right, down, left, up priority
    neighbors = [(x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y), (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
    availableNeighbors = []

    for neighbor in neighbors:
        if neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < wrld.width() and neighbor[1] < wrld.height():
            if wrld.wall_at(neighbor[0], neighbor[1]) != True:
                availableNeighbors.append(neighbor)

    return availableNeighbors
            

def heuristics(start, goal):
    '''
    :param start [int, int]
    :param goal  [int, int]
    :return euclidean distance.
    '''
    return math.sqrt(pow(abs(start[0] - goal[0]), 2) + pow(abs(start[1] - goal[1]), 2))

def astar(character, wrld):
    '''
    :param wrld  [SensedWorld] world object
    :return path [[(int, int)]] fastest path from current to goal
    '''
    start = (character.x, character.y)
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

        nextNodes = neighbors_of_8(character, wrld, current[0], current[1])
        for nextNode in nextNodes:
            new_cost = cost[current] + cost_to_visit_node
            if nextNode not in cost or new_cost < cost[nextNode]:
                cost[nextNode] = new_cost
                priority = new_cost + heuristics(nextNode, goal)
                queue.put(nextNode, priority)
                cameFrom[nextNode] = current
    
    # We make our path
    while current != start:
        path.insert(0, current)
        current = cameFrom[current]

    return path
