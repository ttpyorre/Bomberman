# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../team02')
from testcharacter import TestCharacter
from expectimaxcharacter import ExpectimaxCharacter


# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
g.add_character(ExpectimaxCharacter("Tom", # name
                              "C",  # avatar
                              0, 0  # position
))

# Run!
g.go(1)
