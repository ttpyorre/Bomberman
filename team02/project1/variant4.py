#!/usr/bin/env Python3
# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster
from minimax_character import MinimaxCharacter

# TODO This is your code!
sys.path.insert(1, '../team02')
from testcharacter import TestCharacter

# Create the game
random.seed(123) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    0, 3,        # position
                                    2             # detection range
))

# TODO Add your character
g.add_character(MinimaxCharacter("me", # name
                              "C",  # avatar
                              2, 4  # position
))

# Run!
g.go(1)
