# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../teamNN')
from testcharacter import TestCharacter
from minimaxCharacter import MinimaxCharacter
from bombermanCharacter import BombermanCharacter


# Create the game
g = Game.fromfile('map.txt')

# # TODO Add your character
# g.add_character(TestCharacter("me", # name
#                               "C",  # avatar
#                               0, 0  # position
# ))

g.add_character(BombermanCharacter("mini", # name
                              "C",  # avatar
                              0, 2  # position
))

# Run!
g.go()
