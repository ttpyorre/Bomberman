# Basic functions we might call for a lot
import sys
sys.path.insert(0, '../bomberman')

from colorama import Fore, Back

# get PriorityQueue
from priorityQueue import PriorityQueue
from entity import CharacterEntity
import numpy as np
import math


def neighbors_of_4(wrld, x, y):
    '''
    Returns walkable neighbor cells of the cell we are currently in.
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

def neighbors_of_4_corners(wrld, x, y, ignore_walls = False):
    '''
    Returns walkable neighboring corner cells of the cell we are currently in.
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

def euclidean(start, goal):
    '''
    :param start [int, int]
    :param goal  [int, int]
    :return euclidean distance to goal
    '''
    return math.sqrt(pow(abs(start[0] - goal[0]), 2) + pow(abs(start[1] - goal[1]), 2))
    

def heuristics(start, goal):
    '''
    :param start [int, int]
    :param goal  [int, int]
    :return astar heuristics value.
    '''
    return euclidean(start, goal)

def astar(character, wrld, goal = None, ignore_walls = False):
    '''
    :param wrld         [SensedWorld] world object
    :param ignore_walls [Bool] do we ignore walls in out path
    :return path        [[(int, int)]] fastest path from current to goal
    '''
    start = (character.x, character.y)

    if goal == None:
        goal = wrld.exitcell
    else:
        goal = goal

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

        nextNodes = neighbors_of_8(wrld, current[0], current[1], ignore_walls)
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

def num_walls(wrld, character):
    """
    Uses astar to calc the number of walls between x,y and the exit cell
    """

    path = astar(character, wrld, wrld.exitcell, True)
    
    walls = 0

    for p in path:
        if wrld.wall_at(p[0], p[1]):
            walls += 1

    return walls

def in_range_of_bomb(wrld, x, y):
    
    range = 4
    
    try:
        bomb = next(iter(wrld.bombs.values()))
    except:
        print("no bomb")
        return False

    dx = abs(bomb.x - x)
    dy = abs(bomb.y - y)
    
    if dx <= range or dy <= range:
        return True
    else:
        return False
    
def is_bomb_active(wrld):

    try:
        bomb = next(iter(wrld.bombs.values()))
        print("bomb true")
        return True
    except:
        print("bomb false")
        return False

def explosions_exist(wrld):
    try:
        ex = next(iter(wrld.explosions.values()))
        print("ex exist")
        return True
    except:
        # No bomb
        print("ex nope")
        return False
    
def num_neighboring_explosions(wrld, x, y):
    """
    Returns the num of neighboring cells with a bomb
    """

    neighbors = neighbors_of_8(wrld, x, y)

    count = 0

    for n in neighbors:
        if wrld.explosion_at(n[0], n[1]) != None:
            # if not None, then there is an explosion there
            count += 1
    
    return count



