#!/urs/bin/env Python3
# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../team02')
from testcharacter import TestCharacter
from selfPreserveCharacterMult import SelfPreserveCharacterMult
from bugTest_multMonst import BugTestVar5


# Create the game
random.seed(9) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(StupidMonster("stupid", # name
                            "S",      # avatar
                            3, 5,     # position
))
g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    3, 13,        # position
                                    1             # detection range
))
'''
# Our AI
g.add_character(SelfPreserveCharacterMult("minimax-multi", # name
                              "C",  # avatar
                              0, 0  # position
))
'''
# bug testing
g.add_character(BugTestVar5("minimax-multi", # name
                              "C",  # avatar
                              0, 0  # position
))

# Run!
g.go(1)
