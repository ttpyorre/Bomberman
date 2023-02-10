#!/usr/bin/env Python3
# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../team02')
sys.path.insert(1, './charactersP1')
from aggCharacter import AggCharacter
from selfPreserveCharacter import SelfPreserveCharacter
from interactivecharacter import InteractiveCharacter
from interactiveEventBug import InteractiveCharacterBugSearch

# Create the game
random.seed(123456789) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')

g.add_monster(SelfPreservingMonster("selfpreserving", # name
                                    "S",              # avatar
                                    3, 9,             # position
                                    1                 # detection range
))

'''
g.add_character(InteractiveCharacterBugSearch("Bug-Hunter", # name
                             "C",  # avatar
                             0, 0  # position
))
'''

# Our AI character
g.add_character(SelfPreserveCharacter("minimax", # name
                              "C",  # avatar
                              0, 0  # position
))

'''
g.add_character(AggCharacter("minimax-aggro", # name
                              "C",  # avatar
                              0, 0  # position
))
'''

# Run!
g.go(1)
