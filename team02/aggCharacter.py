# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import search

class AggCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        path = search.astar(self, wrld)
        while path:
            walk = path.pop()
            self.move(walk[0] - self.x, walk[1] - self.y)

    def minimax(self):
        pass

    def max_val(self, wrld):
        if self.terminal_state(wrld):
            return self.terminal_utility(wrld)
        


        pass

    def min_val(self, wrld):
        if self.terminal_state(wrld):
            return self.terminal_utility(wrld)



        pass

    def terminal_state(self, wrld):
        '''
        '''
        # look at ALL monsters
        if wrld.monsters_at(self.x, self.y):
            return True


        if wrld.exit_at(self.x, self.y):
            return True

        return False

    def terminal_utility(self, wrld):
        '''
        '''
        # look at ALL monsters
        if wrld.monsters_at(self.x, self.y):
            return -10


        if wrld.exit_at(self.x, self.y):
            return 10

        return 0
        


