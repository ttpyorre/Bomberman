# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from sensed_world import SensedWorld
from events import Event
from colorama import Fore, Back
import copy
from math import dist

class MinimaxCharacter(CharacterEntity):
    
    # def __init__(self, x, y):
    # this is handled by character enity fucntion
    #     self.x = x
    #     self.y = y

    def do(self, world):
        # if self.terminal_state(world):
        #     print("Hell yes the world is ending")
        # pass
        print(self.minimax_decision(world))
        
        # self.result(world, (1, 1))
        # print(self.x, self.y)
        
        # self.move(1,0)
        # actions = self.actions(world)
        # for a in actions: print(a)

        # world_copy = SensedWorld.from_world(world)
        # (new_world, events) = world_copy.next()
        # for e in events:
        #     print(e.tpe = Event.IS_KILLED_BY_MONSTER)
        # pass
        

    def minimax_decision(self, world):
        
        actions = self.actions(world)
        # best_move = doing nothing
        v = -100
        for a in actions:
            calc_v = self.min_value(self.result(world, a))
            
            if calc_v > v:
                v = calc_v
                best_a = a
        return best_a

    def max_value(self, world):
        # return a utility value
        actions = self.actions(world)
        v = -100.0
        if self.terminal_state(world): return self.utility(world)
        for a in actions:
            v = max([v, self.min_value(self.result(world, a))])
        return v

    def min_value(self, world):
        # return a utility value
        
        # print(world.width(), world.height())
        actions = self.actions(world)
        v = 100.0
        if self.terminal_state(world): return self.utility(world)
        for a in actions:
            v = max([v, self.max_value(self.result(world, a))])
        return v

    def terminal_state(self, world):
        # we should check if we are at the exit or attacked by the monsiter
        print("enter")
        # monster
        return world.monsters_at(self.x, self.y) or world.exit_at(self.x, self.y)
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

        char = next(iter(world.characters.values()))[0]
        char_neighbors = self.neighbors(world, char.x, char.y)

        # looking through each monster
        for monster in next(iter(world.monsters.values())):
            mon_neighbors = self.neighbors(world, monster.x, monster.y)

            # comparing each neightboring cell of the monster with the character
            for char_neighbor in char_neighbors:
                for mon_neighbor in mon_neighbors:
                    if char_neighbor == mon_neighbor: 
                        u -= 1.0
                        # print("n")


                # # comparing if the monster is next to the character
                # print("c: " + str(char_neighbor))
                # print("M: " + str((monster.x, monster.y)))
                # if char_neighbor == (monster.x, monster.y): 
                #     u -= 2
                #     print("n2")

        # considering the exit, I am lazy. Lets just use the eucliedean distance
        u += dist(world.exitcell, (char.x, char.y))

        return u

    def result(self, world, action):
        # returns the new new world resulting from the action at
        # new_world = copy.deepcopy(world)
        world_copy = SensedWorld.from_world(world)
        char = next(iter(world_copy.characters.values()))[0]   # returns a list of characters
        char.move(action[0], action[1])                  # since there is only 1 character in the list, just take the first element
        (world_copy_2, events) = world_copy.next()          # creates a new world with the applied action

        # bugging purposes -> if we want to see the resulting state
        # world_copy_2.printit()

        return world_copy_2

    def actions(self, world):
        
        # Works

        # returns the possibe actions that can be performed
        return self.neighbors(world, self.x, self.y)

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