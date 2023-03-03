# This is necessary to find the main code
import sys
sys.path.insert(0, '../Bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from events import Event
import math
from priorityQueue import PriorityQueue
import numpy as np

class QLearningCharacter(CharacterEntity):

    # weights = [0.3*3.2240646069681054, ]
    w1 = 0.3*3.2240646069681054
    w2 = 0.4*0.28043526385758355
    w3 = 0.01

    STATE=0

    EXPLORING = 0
    EXPLORE_WALL = 1
    BOMBING = 2
    RUNNING = 3
    WAITING = 4
    KEEPWAITING = 5

    TESTING = 6

    def do(self, wrld):
        # self.w1 = 0.3 * weight1
        # self.w2 = 0.4 * weight2
        self.alpha = 0.8
        self.decay = 0.9

        
        if self.STATE == self.BOMBING:
            self.place_bomb()
            self.move(0, 0)
            # Go into Running state
            self.STATE = self.RUNNING
            return
        elif self.STATE == self.RUNNING:
            runs = QLearningCharacter.neighbors_of_4_corners(wrld, self.x, self.y)
            run = runs[0]
            where = np.subtract(run, (self.x, self.y))
            self.move(where[0], where[1])
            self.STATE = self.WAITING
            return
        elif self.STATE == self.WAITING:
            self.move(0, 0)
            self.STATE = self.EXPLORING
            return
        elif self.STATE == self.KEEPWAITING:
            self.move(0, 0)
            self.STATE = self.EXPLORING
            return

        elif self.STATE == self.EXPLORING:
            
            # case _:
            #     pass
            print("Exploring")
            if self.wall_nearby(wrld, self.x, self.y):
                # return self.BOMBING, self.w1, self.w2
                self.STATE = self.BOMBING
                print(self.STATE)
                return
            char = next(iter(wrld.characters.values()))[0]

            if wrld.monsters.values():
                mons = next(iter(wrld.monsters.values()))[0]

            maxQ = float("-inf")
            action = (0, 0)
            for a in self.getLegalActions(0, wrld):
                #print(a)
                char.move(a[0], a[1])
                (newwrld,events) = wrld.next()
                # utility = exp_value(0, newwrld, events)
                Q = self.q_Learning(self.w1, self.w2, self.w3, newwrld)

                if Q >= maxQ or maxQ == float("-inf"):
                    maxQ = Q
                    action = a

            self.move(action[0], action[1])
            (newwrld, events) = wrld.next()
            # Check if character is at the exit after moving
            if newwrld.characters.values():
                if next(iter(newwrld.characters.values())):
                    newChar = next(iter(newwrld.characters.values()))[0]   
                else:
                    delta = abs(newwrld.scores[char.name]) + 5000 - maxQ
                    self.w1 = self.w1 + self.alpha * delta * 1
                    if wrld.monsters.values():
                        tempChar = char
                        tempChar.x = wrld.exitcell[0]
                        tempChar.y = wrld.exitcell[1]
                        f2 = self.feature_rep(tempChar, wrld, 2)
                    else:
                        f2 = 1
                    
                    self.w2 = self.w2 + self.alpha * delta * f2

                    # return (self.EXPLORING, 0.3 * self.w1, 0.3 * self.w2)
                    self.STATE = self.EXPLORING
                    return
            else:
                delta = abs(newwrld.scores[char.name]) - maxQ
                self.w1 = self.w1 + self.alpha * delta * 1
                if wrld.monsters.values():
                    tempChar = char
                    tempChar.x = wrld.exitcell[0]
                    tempChar.y = wrld.exitcell[1]
                    f2 = self.feature_rep(tempChar, wrld, 2)
                else:
                    f2 = 1
                
                self.w2 = self.w2 + self.alpha * delta * f2

                # return (self.EXPLORING, 0.3 *  self.w1, 0.3 * self.w2)
                self.STATE = self.EXPLORING
                return

            # Calculate maxQPrime for delta calculations
            maxQprime = float("-inf")
            for a in self.getLegalActions(0, newwrld):
                newChar.move(a[0], a[1])
                (Qwrld,events) = wrld.next()
                # utility = exp_value(0, newwrld, events)
                Q = self.q_Learning(self.w1, self.w2, self.w3, Qwrld)

                if Q >= maxQprime or maxQprime == float("-inf"):
                    maxQprime = Q

            delta = ( abs(newwrld.scores[char.name]) + self.decay * maxQprime) - maxQ

            f1 = self.feature_rep(char, wrld, 1)
            self.w1 = self.w1 + self.alpha * delta * f1

            if wrld.monsters.values():
                f2 = self.feature_rep(char, wrld, 2)
            else:
                f2 = 1
            
            self.w2 = self.w2 + self.alpha * delta * f2


            f3 = self.feature_rep(char, wrld, 3)
            self.w3 = self.w3 + self.alpha * delta * f3
            

            # print((self.w1, self.w2))

            # return (self.EXPLORING, 0.3 * self.w1, 0.3 * self.w2)
            self.STATE = self.EXPLORING
            return
    
    
    
    def feature_rep(self, char, wrld, x):
        

        # match x:
        #     case 1:
                # Distance to exit
        path = QLearningCharacter.astar(char, wrld)
        if x == 1:
            if wrld.exitcell not in path:
                return 1 / pow((1 + QLearningCharacter.heuristics((char.x, char.y), wrld.exitcell)), 2)
            else:
                return 1 / pow(1 + len(path), 2)
                # return 1 / pow((1 + QLearningCharacter.heuristics((char.x, char.y), wrld.exitcell)), 2)           
        if x == 2:
            # Distance to monster
            mons = next(iter(wrld.monsters.values()))[0]
            return 1 / pow((1 + QLearningCharacter.heuristics((char.x, char.y), (mons.x, mons.y))), 3)
        if x == 3:
            # Corners of the character
            # corners = self.neighbors_of_4_corners(wrld, char.x, char.y)
            # return 1 / (1 + len(corners)) 
            return 1
            
    def q_Learning(self, w1, w2, w3, wrld):
        if wrld.characters.values():
            if next(iter(wrld.characters.values())):
                char = next(iter(wrld.characters.values()))[0]      
                f1 = self.feature_rep(char, wrld, 1)
                f3 = self.feature_rep(char, wrld, 3)
            else:
                f1 = 1
                f3 = 1
        else:
            f1 = 1
            f3 = 1

        if wrld.monsters.values():
            mons = next(iter(wrld.monsters.values()))[0]
            if wrld.characters.values():
                if next(iter(wrld.characters.values())):
                    f2 = self.feature_rep(char, wrld, 2)
                else: 
                    f2 = 1
            else:
                f2 = 1
        else:
            f2 = 1

        Q = w1 * f1 - w2 * f2 - w3 * f3
        return Q

        
    @staticmethod
    def neighbors_of_4_corners(wrld, x, y):
    # we search with right, down, left, up priority
        neighbors = [(x + 1, y + 1), (x - 1, y + 1), (x - 1, y - 1), (x + 1, y - 1)]
        availableNeighbors = []

        for neighbor in neighbors:
            if neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < wrld.width() and neighbor[1] < wrld.height():
                if not wrld.wall_at(neighbor[0], neighbor[1]) or not (wrld.monsters_at(neighbor[0], neighbor[1]) is None):
                    availableNeighbors.append(neighbor)

        return availableNeighbors

    def wall_nearby(self, wrld, x, y):
        neighbors = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        for neighbor in neighbors:
            if neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < wrld.width() and neighbor[1] < wrld.height():
                if wrld.wall_at(neighbor[0], neighbor[1]):
                    return True
                
        return False
    
    @staticmethod
    def neighbors_of_8(wrld, x, y):
        '''
        Returns walkable neighbor cells of the cell we are currently in.
        :param wrld     [SensedWorld]   world object
        :param x        [int]           x coordinate in world
        :param y        [int]           y coordinate in world
        :return         [[(int, int)]]  list of all neighbors that are available
        '''
        # we search with right, down, left, up priority
        neighbors = [(x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y), (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
        availableNeighbors = []

        for neighbor in neighbors:
            if neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < wrld.width() and neighbor[1] < wrld.height():
                if wrld.wall_at(neighbor[0], neighbor[1]) != True:
                    availableNeighbors.append(neighbor)

        return availableNeighbors

    @staticmethod
    def heuristics(start, goal):
        return math.sqrt(pow(abs(start[0] - goal[0]), 2) + pow(abs(start[1] - goal[1]), 2))

    @staticmethod
    def astar(char, wrld):
        start = (char.x, char.y)
        goal = wrld.exitcell

        # Establishing our queue
        queue = PriorityQueue()
        queue.put(start, 0)
        
        cameFrom = {}
        cost = {}
        cost_to_visit_node = 1
        cameFrom[start] = None
        cost[start] = 0

        path = []

        while not queue.empty():
            current = queue.get()

            if goal == current: # found goal
                break

            nextNodes = QLearningCharacter.neighbors_of_8(wrld, current[0], current[1])
            for nextNode in nextNodes:
                new_cost = cost[current] + cost_to_visit_node # cost is length of nodes + 
                if wrld.wall_at(nextNode[0], nextNode[1]) or not (wrld.monsters_at(nextNode[0], nextNode[1]) is None):
                    new_cost += 1 
                if nextNode not in cost or new_cost < cost[nextNode]:
                    cost[nextNode] = new_cost
                    priority = new_cost + QLearningCharacter.heuristics(nextNode, goal)
                    queue.put(nextNode, priority)
                    cameFrom[nextNode] = current
        
        # We make our path
        while current != start:
            path.insert(0, current)
            current = cameFrom[current]
        
        return path
    
    # Character has index 0 and monsters have index >= 1
    def getLegalActions(self, charIndex, wrld):
        legalActions = []

        if charIndex == 0: 
            e = next(iter(wrld.characters.values()))[0]
        else:
            if wrld.monsters.values():
                e = next(iter(wrld.monsters.values()))[0]

        # Go through the possible 8-moves of the entity
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (e.x + dx >= 0) and (e.x + dx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Make sure the monster is moving
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (e.y + dy >= 0) and (e.y + dy < wrld.height()):
                            # No need to check impossible moves
                            if not wrld.wall_at(e.x + dx, e.y + dy):
                                if charIndex == 0:
                                    if not wrld.monsters_at(e.x + dx, e.y + dy):
                                        if not wrld.explosion_at(e.x + dx, e.y + dy):
                                            legalActions.append([dx, dy])
                                else:
                                    legalActions.append((dx, dy))

        return legalActions 