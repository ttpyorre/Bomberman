# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from events import Event
import math
from priorityQueue import PriorityQueue
import numpy as np

class ExpectimaxCharacter(CharacterEntity):
    EXPLORING = 0
    EXPLORE_WALL = 1
    BOMBING = 2
    RUNNING = 3
    WAITING = 4
    KEEPWAITING = 5
 

    def do(self, wrld, state):
        self.w1 = 1
        self.w2 = 2
        self.alpha = 0.9
        self.decay = 0.9
        print(state)
        match state:
            case self.BOMBING:
                self.place_bomb()
                self.move(0, 0)
                # Go into Running state
                return self.RUNNING
            case self.RUNNING:
                runs = ExpectimaxCharacter.neighbors_of_4_corners(wrld, self.x, self.y)
                run = runs[0]
                where = np.subtract(run, (self.x, self.y))
                self.move(where[0], where[1])
                return self.WAITING
            case self.WAITING:
                self.move(0, 0)
                return self.KEEPWAITING
            case self.KEEPWAITING:
                self.move(0, 0)
                return self.EXPLORING
            case self.EXPLORING:
                pass
            case _:
                pass

        if self.wall_nearby(wrld, self.x, self.y):
            return self.BOMBING
        char = next(iter(wrld.characters.values()))[0]
        # path = ExpectimaxCharacter.astar(char, wrld)
        # if wrld.exitcell not in path:
        #     print("NOT FOUND")
        # else:
        #     print("FOUND")
        
        if wrld.monsters.values():
            mons = next(iter(wrld.monsters.values()))[0]

        # Character has index 0 and monsters have index >= 1
        def getLegalActions(charIndex, wrld):
            legalActions = []

            if charIndex == 0: 
                e = char
            else:
                e = mons

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
                                            legalActions.append([dx, dy])
                                    else:
                                        legalActions.append((dx, dy))

            return legalActions

        def max_value(depth, world, events):
            for event in events:
                # print(event)
                if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER or event.tpe == Event.BOMB_HIT_CHARACTER:
                    return world.scores[char.name] - 10000
                elif event.tpe == Event.CHARACTER_FOUND_EXIT:
                    return world.scores[char.name] + 10000
                   
            Q = self.q_Learning(self.w1, self.w2, world)
            char_max = next(iter(world.characters.values()))[0]

            if depth == 2:
                path = ExpectimaxCharacter.astar(char_max, world)
                if wrld.exitcell not in path:
                    return world.scores[char_max.name] - ExpectimaxCharacter.heuristics((char_max.x, char_max.y), wrld.exitcell) - Q
                else:
                    return world.scores[char_max.name] - len(path) - Q

            v = float("-inf")
            maxq = float("-inf")
            for a in getLegalActions(0, world):
                char.move(a[0], a[1])
                # print(a)
                (newwrld, newevents) = world.next()
                v = max(v, exp_value(depth + 1, newwrld, newevents))
                maxq = max(maxq, self.q_Learning(self.w1, self.w2, newwrld))
            delta = (v + self.decay * maxq) - Q
            self.w1 = self.w1 + self.alpha * delta * 1/(1+ExpectimaxCharacter.heuristics((char_max.x, char_max.y), wrld.exitcell))
            if world.monsters.values():
                mons = next(iter(world.monsters.values()))[0]
                self.w2 = self.w2 + self.alpha * delta * 1/(1+ExpectimaxCharacter.heuristics((char_max.x, char_max.y), (mons.x, mons.y)))                
            return v

        def exp_value(depth, world, events):
            for event in events:
                # print(event)
                if event.tpe == Event.BOMB_HIT_CHARACTER or event.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                    return world.scores[char.name] - 10000
                elif event.tpe == Event.CHARACTER_FOUND_EXIT:
                    return world.scores[char.name] + 10000

            Q = self.q_Learning(self.w1, self.w2, world)
            if world.monsters.values():
                mons_exp = next(iter(world.monsters.values()))[0]
            char_exp = next(iter(world.characters.values()))[0]

            if depth == 2:
                path = ExpectimaxCharacter.astar(char_exp, world)
                if wrld.exitcell not in path:
                    return world.scores[char_exp.name] - ExpectimaxCharacter.heuristics((char_exp.x, char_exp.y), wrld.exitcell) - Q
                else:
                    return world.scores[char_exp.name] - len(path) - Q
                
            v = 0
            maxq = float("-inf")
            if world.monsters.values():
                p = 1.0 / len(getLegalActions(1, world))
                for a in getLegalActions(1, world):
                    # print(a)
                    mons_exp.move(a[0], a[1])
                    (newwrld, newevents) = world.next()
                    v = v + p * max_value(depth + 1, newwrld, newevents)
                    maxq = max(maxq, self.q_Learning(self.w1, self.w2, newwrld))
                delta = (v + self.decay * maxq) - Q
                self.w1 = self.w1 + self.alpha * delta * 1/(1+ExpectimaxCharacter.heuristics((char_exp.x, char_exp.y), wrld.exitcell))
                self.w2 = self.w2 + self.alpha * delta * 1/(1+ExpectimaxCharacter.heuristics((char_exp.x, char_exp.y), (mons_exp.x, mons_exp.y)))    
                return v
            else:
                p = 1.0 / len(getLegalActions(0, world))
                for a in getLegalActions(0, world):
                    # print(a)
                    char_exp.move(a[0], a[1])
                    (newwrld, newevents) = world.next()
                    v = v + p * max_value(depth + 1, newwrld, newevents)
                    maxq = max(maxq, self.q_Learning(self.w1, self.w2, newwrld))
                delta = (v + self.decay * maxq) - Q
                self.w1 = self.w1 + self.alpha * delta * 1/(1+ExpectimaxCharacter.heuristics((char_exp.x, char_exp.y), wrld.exitcell))
                return v
            
        maximum = float("-inf")
        action = (0, 0)
        for a in getLegalActions(0, wrld):
            #print(a)
            char.move(a[0], a[1])
            (newwrld,events) = wrld.next()
            utility = exp_value(0, newwrld, events)
            #print(utility)
            if utility >= maximum or maximum == float("-inf"):
                maximum = utility
                action = a

        self.move(action[0], action[1])

        return self.EXPLORING
    
    def q_Learning(self, w1, w2, wrld):
        if wrld.characters.values():
            if next(iter(wrld.characters.values())):
                char = next(iter(wrld.characters.values()))[0]      
                f1 = 1/(1+ExpectimaxCharacter.heuristics((char.x, char.y), wrld.exitcell))
            else:
                return 0
        else:
            return 0

        if wrld.monsters.values():
            mons = next(iter(wrld.monsters.values()))[0]
            f2 = 1/(1+ExpectimaxCharacter.heuristics((char.x, char.y), (mons.x, mons.y)))
        else:
            f2 = 0

        Q = w1 * f1 + w2 * f2
        return Q

        
    
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

            nextNodes = ExpectimaxCharacter.neighbors_of_8(wrld, current[0], current[1])
            for nextNode in nextNodes:
                new_cost = cost[current] + cost_to_visit_node # cost is length of nodes + 
                if wrld.wall_at(nextNode[0], nextNode[1]) or not (wrld.monsters_at(nextNode[0], nextNode[1]) is None):
                    new_cost += 1 
                if nextNode not in cost or new_cost < cost[nextNode]:
                    cost[nextNode] = new_cost
                    priority = new_cost + ExpectimaxCharacter.heuristics(nextNode, goal)
                    queue.put(nextNode, priority)
                    cameFrom[nextNode] = current
        
        # We make our path
        while current != start:
            path.insert(0, current)
            current = cameFrom[current]
        
        return path