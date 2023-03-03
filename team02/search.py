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
    
    brange = 4
    
    try:
        bomb = next(iter(wrld.bombs.values()))
        # print("Yay boimb")
    except:
        # print("no bomb")
        return False
    

    for dx in range(-brange, brange+1):
        for dy in range(-brange, brange+1):
            # print("(x, y): " + str((x, y)) + " " + str((bomb.x + dx, bomb.y + dy)))
            
            if (x, y) == (bomb.x + dx, bomb.y):
                return True
            
            if (x, y) == (bomb.x, bomb.y + dy):
                return True
    
    return False

    # dx = abs(bomb.x - x)
    # dy = abs(bomb.y - y)

    # print("dx:" + str(dx))
    # print("dy:" + str(dy))
    
    # if dx <= range or dy <= range:
    #     return True
    # else:
    #     return False
    
def wall_in_range_of_bomb(wrld):
    
    brange = 4
    
    try:
        bomb = next(iter(wrld.bombs.values()))
    except:
        # print("no bomb")
        return False

    for dy in range(-brange, brange+1):
        if wrld.wall_at(bomb.x, bomb.y + dy): 
            return True
    
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


def get_char_available_actions(wrld, x, y):
    """
    Gets the available moves at position x, y, and us of bombs
        Note, only checks for walls, or out of bounds
    """ 

    # check to see if a bomb exist

    bomb_exist = False

    try:
        bomb = next(iter(wrld.bombs.values()))[0]
        bomb_exist = True
    except:
        print("no bombs exist")
    
    actions = []

    for dx in [-1, 0, 1]:
        if x + dx >= 0 and x + dx < wrld.width():
            for dy in [-1, 0, 1]:
                if (dx != 0 or dy != 0) and y + dy >= 0 and y + dy < wrld.height():
                    if not wrld.wall_at(x + dx, y + dy):

                        # add as a possible action to place a bomb and move
                        # regardless of the situation, we should be allowed to move without placing a bomb
                        actions.append((dx, dy, False))

                        if not bomb_exist:
                            # give myself the option to place a bomb
                            actions.append((dx, dy, True))

    return actions

def get_all_possible_actions():
    """
    Gets all possible actions the char can do. Doesnt IGNORE any actions.
        Doesnt care about:
            Out of bounds
            Walls
            Monsters
            Bombs
            Explosions
    """
    actions = []

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for use_bomb in [True, False]:
                actions.append((dx, dy, use_bomb))
    return actions



