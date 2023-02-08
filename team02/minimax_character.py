# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from sensed_world import SensedWorld
from events import Event
from colorama import Fore, Back
from priorityQueue import PriorityQueue
import copy
import math

class MinimaxCharacter(CharacterEntity):
    
    # def __init__(self, x, y):
    # this is handled by character enity fucntion
    #     self.x = x
    #     self.y = y

    def do(self, world):
        # self.move(1, 0)
        # print(self.actions(world))
        # print(self.non_terminal_utility(world))
        
        (x, y) = self.minimax_decision(world)
        self.move(x, y)
        
        self.move_to_exit(world)

        # self.min_value(None)
        pass

    def move_to_exit(self, world):
        exit = world.exitcell 
        exit_neighbors = self.neighbors_of_8(world, exit[0], exit[1])
        
        print((self.x, self.y))
        # force the character to move toward the exit
        for n in exit_neighbors:
            print("n: " + str(n)+ " util: "+str(self.non_terminal_utility(world)))
            if (self.x, self.y) == n:
                dx = exit[0] - self.x
                dy = exit[1] - self.y
                self.move(dx, dy)
        

    def minimax_decision(self, world):
        char = self.get_char(world)

        actions = self.actions(world)
        best_a = (0,0)
        v = float("-inf")
        depth = 1
        max_depth = 5
        for a in actions:
            char.move(a[0], a[1])
            (_next_world, events) = world.next()

            calc_v = self.min_value(_next_world, events, depth + 1, max_depth)
            
            if calc_v > v :
                v = calc_v
                best_a = a
        # print(v, str(best_a))
        return best_a

    

    def max_value(self, world, events, depth, max_depth):
        # return a utility value
        actions = self.actions(world)
        v = float("-inf")

        # lets just consider the world passed in
        (isTerminalState, util) = self.terminal_state(world, events, depth, max_depth)
        if isTerminalState: return util

        # its not a terminal state, then we need to consider the next depth
        for a in actions:
            (_new_world, events) = self.result(world, a)
            v = max([v, self.min_value(_new_world, events, depth + 1, max_depth)])
        return v

    def min_value(self, world, events, depth, max_depth):
        # return a utility value
        actions = self.actions(world)
        v = float("inf")

        # lets just consider the world passed in
        (isTerminalState, util) = self.terminal_state(world, events, depth, max_depth)
        if isTerminalState: return util

        # its not a terminal state, then we need to consider the next depth
        for a in actions:
            (_new_world, events) = self.result(world, a)
            v = min([v, self.max_value(_new_world, events, depth + 1, max_depth)])
        return v

    def terminal_state(self, world, events, depth, max_depth):
        # if the terminal state returns nothing, then we should be good
        # other wise we should handle it better

        try:
            char = self.get_char(world)

            if depth >= max_depth:
                return (True, self.non_terminal_utility(world))

            for event in events:

                if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER or event.tpe == Event.BOMB_HIT_CHARACTER:
                    return (True, float(world.scores[char.name] - 1000000))
                elif event.tpe == Event.CHARACTER_FOUND_EXIT:
                    return (True, float(world.scores[char.name] + 1000000))
        except:
            return (True, -10000000.0)
        
        # there is no terminal event that occured
        return (False, None)
   
    def non_terminal_utility(self, world):
        char = self.get_char(world)
        exit = world.exitcell
        # mon = self.get_monster(world)

        u = float(world.scores[char.name])

        # looking through each monster
        for monster in next(iter(world.monsters.values())):
            u += 10.0*math.dist((char.x, char.y), (monster.x, monster.y))
            
        try:
            path_len = len(self.astar(char, world))
            
        except:
            # not really too sure, somehow it is passed a None World
            path_len = 0
        
        if path_len >= 3: 
            u -= float(8*path_len)
            u -= float(10*math.dist((char.x, char.y), (exit[0], exit[1])))
        else:
            u -= float(14*math.dist((char.x, char.y), (exit[0], exit[1])))
            # for monster in next(iter(world.monsters.values())):
            #     u += 3.0*math.dist((char.x, char.y), (monster.x, monster.y))


        # The len of the path close to the goal
        # at the end only causes more issues than it helps
            

        # there are multiple points where the lenght of astar is the same
        
        return u

    def result(self, world, action):
        # returns the new new world resulting from the action at
        # new_world = copy.deepcopy(world)
        char = self.get_char(world)   
        char.move(action[0], action[1])                  
        return world.next()  
        # try:
                    

        # except:
        #     print("The character is dead already")
        #     return (None, None)

    def actions(self, world):
        
        # Works

        # returns the possibe actions that can be performed
        a = []
        for n in self.neighbors_of_8(world, self.x, self.y):
            a.append((n[0]-self.x, n[1]-self.y))
        return a

    # def neighbors(self, world, cell_x, cell_y):
        
    #     # get the valid neighbors of a cell
    #     #   has to not be an empty cell
    #     #   has to be inbounds

    #     def within_bounds(x_, y_):
    #         if x_ >= 0 and x_ < world.width():
    #             if y_ >=0 and y_< world.height():
    #                 return True
    #         return False

    #     n = []
        
    #     for dx in [-1, 0, 1]:
    #         for dy in [-1, 0, 1]:
    #             x = cell_x + dx
    #             y = cell_y + dy
    #             if within_bounds(x, y):
    #                 if world.empty_at(x, y):
    #                     n.append((x, y))

        return n

    @staticmethod
    def get_char(world):
        """Return the character"""
        return next(iter(world.characters.values()))[0]

    # @staticmethod
    # def get_monster(world):
    #     """Return monster[s]"""
    #     return next(iter(world.monsters.values()))[0]
        
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

        exploredMap = []
        path = []

        while not queue.empty():
            current = queue.get()

            if goal == current: # found goal
                break

            nextNodes = MinimaxCharacter.neighbors_of_8(wrld, current[0], current[1])
            for nextNode in nextNodes:
                new_cost = cost[current] + cost_to_visit_node # cost is length of nodes + 
                if nextNode not in cost or new_cost < cost[nextNode]:
                    cost[nextNode] = new_cost
                    priority = new_cost + MinimaxCharacter.heuristics(nextNode, goal)
                    queue.put(nextNode, priority)
                    cameFrom[nextNode] = current
        
        # We make our path
        while current != start:
            path.insert(0, current)
            current = cameFrom[current]

        return path