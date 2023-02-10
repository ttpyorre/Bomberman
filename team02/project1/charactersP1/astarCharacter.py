# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

# We are reliant on search for astar
import search

class AstarCharacter(CharacterEntity):

    def do(self, wrld):
        # Astar gives us a path of nodes that we visit one by one
        path = search.astar(self, wrld)
        while path:
            walk = path.pop()
            self.move(walk[0] - self.x, walk[1] - self.y)
