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

        (x, y) = self.minimax_decision(world)
        self.move(x, y)
        exit = world.exitcell 
        exit_neighbors = self.neighbors_of_8(world, exit[0], exit[1])
        
        print((self.x, self.y))
        # force the character to move toward the exit
        for n in exit_neighbors:
            print("n: " + str(n))
            if (self.x, self.y) == n:
                dx = exit[0] - self.x
                dy = exit[1] - self.y
                self.move(dx, dy)
            
        # print(len(self.astar(self, world)))
        pass
        

    def minimax_decision(self, world):
        
        actions = self.actions(world)
        best_a = (0,0)
        v = -100
        depth = 1
        max_depth = 5
        for a in actions:
            calc_v = self.min_value(self.result(world, a), depth + 1, max_depth)
            
            if calc_v > v:
                v = calc_v
                best_a = a
        # print(v, str(best_a))
        return best_a

    def max_value(self, world, depth, max_depth):
        # return a utility value
        actions = self.actions(world)
        v = -100.0
        if self.terminal_state(world) or depth == max_depth: return self.utility(world)
        for a in actions:
            v = max([v, self.min_value(self.result(world, a), depth + 1, max_depth)])
        return v

    def min_value(self, world, depth, max_depth):
        # return a utility value
        
        # print(world.width(), world.height())
        actions = self.actions(world)
        v = 100.0
        if self.terminal_state(world) or depth == max_depth: return self.utility(world)
        for a in actions:
            v = min([v, self.max_value(self.result(world, a), depth + 1, max_depth)])
        return v

    def terminal_state(self, world):
        # we should check if we are at the exit or attacked by the monsiter
        # monster

        world_copy = SensedWorld.from_world(world)
        (world_copy, events) = world_copy.next()
        
        for e in events:
            if e.tpe == Event.CHARACTER_KILLED_BY_MONSTER or e.tpe == Event.CHARACTER_FOUND_EXIT: return True
        pass

        try:
            char = next(iter(world_copy.characters.values()))[0]
            # print("There is no character")
        except:
            return True

        # return world.monsters_at(self.x, self.y) or world.exit_at(self.x, self.y)
        # bomb blast
        return False
        
    def utility(self, world):
        # the util of the char's position looses -1 for every neighboring space matching the monster
        # the util of the state looses -2 for all monsters in the neighbor of the character

        # include the neighborhoods to define utility
        #   for the neighbors of a monster multiply by -0.5

        # Include the distance calc from a start

        # how about walls
        # lets assume there is no cost

        u = 0.0

        try:
            char = next(iter(world.characters.values()))[0]
            char_neighbors = self.neighbors(world, char.x, char.y)

            # looking through each monster
            for monster in next(iter(world.monsters.values())):
                # mon_neighbors = self.neighbors(world, monster.x, monster.y)

            #     # comparing each neightboring cell of the monster with the character
            #     for char_neighbor in char_neighbors:
            #         for mon_neighbor in mon_neighbors:
            #             if char_neighbor == mon_neighbor: 
            #                 u -= 50.0
            #                 # print("n")
                u += math.dist((char.x, char.y), (monster.x, monster.y))
            


                    # # comparing if the monster is next to the character
                    # print("c: " + str(char_neighbor))
                    # print("M: " + str((monster.x, monster.y)))
                    # if char_neighbor == (monster.x, monster.y): 
                    #     u -= 2
                    #     print("n2")

            # considering the exit, I am lazy. Lets just use the eucliedean distance
            # u += math.dist(world.exitcell, (0, 0)) - math.dist(world.exitcell, (char.x, char.y))
            u -= len(self.astar(char, world))

            if world.exitcell == (char.x, char.y): u += 100
        except:
            u -= 70.0
            pass

        # print(u)
        return u

    def result(self, world, action):
        # returns the new new world resulting from the action at
        # new_world = copy.deepcopy(world)
        world_copy = SensedWorld.from_world(world)
        try:
            char = next(iter(world_copy.characters.values()))[0]   # returns a list of characters
            char.move(action[0], action[1])                  # since there is only 1 character in the list, just take the first element
            (world_copy_2, events) = world_copy.next()          # creates a new world with the applied action

            # bugging purposes -> if we want to see the resulting state
            # world_copy_2.printit()

            return world_copy_2

        except:
            print("The character is dead already")
            return None

        

    def actions(self, world):
        
        # Works

        # returns the possibe actions that can be performed
        a = []
        for n in self.neighbors(world, self.x, self.y):
            a.append((n[0]-self.x, n[1]-self.y))
        return a

    def neighbors(self, world, cell_x, cell_y):
        
        # get the valid neighbors of a cell
        #   has to not be an empty cell
        #   has to be inbounds

        def within_bounds(x_, y_):
            if x_ >= 0 and x_ < world.width():
                if y_ >=0 and y_< world.height():
                    return True
            return False

        n = []
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x = cell_x + dx
                y = cell_y + dy
                if within_bounds(x, y):
                    if world.empty_at(x, y):
                        n.append((x, y))

        return n

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