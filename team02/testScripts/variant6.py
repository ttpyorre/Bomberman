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
from bombermanCharacter2 import BombermanCharacter2





# Create the game
g = Game.fromfile('test_map.txt')

g.add_character(BombermanCharacter2("mini", # name
                              "C",  # avatar
                              3, 0  # position
))

# Run!
g.go()
