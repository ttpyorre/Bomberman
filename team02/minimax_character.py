# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class MinimaxCharacter(CharacterEntity):
    
    # def __init__(self, x, y):
    # this is handled by character enity fucntion
    #     self.x = x
    #     self.y = y

    def do(self, world):
        
        pass

    def minimax_decision(self, world):
        actions = actions(world)
        # best_move = doing nothing
        v = -10
        for a in actions:
            calc_v = self.min_value(self.result(world, a))
            if calc_v > v:
                v = calc_v
                best_a = a
        return best_a

    def max_value(self, world):
        # return a utility value
        actions = actions(world)
        v = -10
        if self.terminal_state(world): return self.utility(world)
        for a in actions:
            v = max([v, self.min_value(self.result(world, a))])
        return v

    def min_value(self, world):
        # return a utility value
        actions = actions(world)
        v = 10
        if self.terminal_state(world): return self.utility(world)
        for a in actions:
            v = max([v, self.max_value(self.result(world, a))])
        return v

    def terminal_state(self, world):
        # we should check if we are at the exit or attacked by the monsiter
        
        # monster
        if world.mosters_at(self.x, self.y) != []:
            return True

        # exit
        if world.exit_at(self.x, self.y) != []:
            return True

        # bomb blast
        return False
        
    def utility(self, world):
        # the value of the world...so +1 if we are at the exit
        # -1 if we are attacked by a monster

        # include the neighborhoods to define utility
        #   for the neighbors of a monster multiply by -0.5
        #   maybe do it for the exit

        # Include the distance calc from a start

        # how about walls

        # monster
        if world.mosters_at(self.x, self.y) != []:
            return -1

        # exit
        if world.exit_at(self.x, self.y) != []:
            return 1

        # bomb blast
        return 0

    def result(self, world, action):
        # returns the new new world resulting from the action at s


        return 0

    def actions(self, world):

        def within_bounds(x_, y_):
            if x_ >= 0 and x_ < world.width():
                if y_ >=0 and y_< world.height():
                    return True
            return False

        a = []
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x = self.x + dx
                y = self.y + dy
                if within_bounds(x, y):
                    if world.empty_at(x, y):
                        a.append((x, y))

        # returns the possibe actions that can be performed
        return a