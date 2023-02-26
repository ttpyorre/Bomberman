# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

# Import Priority Queue
from priorityQueue import PriorityQueue
import numpy as np
import math

class SimulatedAnnealing(CharacterEntity):

    def do(self, wrld):
        # Astar gives us a path of nodes that we visit one by one
        path = self.astar(wrld)
        while path:
            walk = path.pop()
            self.move(walk[0] - self.x, walk[1] - self.y)
    
    
    
    def simulated(self):
        
        
