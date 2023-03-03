# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster

# TODO This is your code!
sys.path.insert(1, '../teamNN')
from testcharacter import TestCharacter
from expectimaxcharacter import ExpectimaxCharacter
from qlearningcharacter import QLearningCharacter

num_win = 0
w1 = 1
w2 = 1

# Create the game
for i in range(100):
    random.seed(i) # TODO Change this if you want different random choices
    g = Game.fromfile('map.txt')
    g.add_monster(StupidMonster("selfpreserving", # name
                                        "S",              # avatar
                                        3, 9,             # position
                                        1                 # detection range
    ))

    # TODO Add your character
    g.add_character(QLearningCharacter("me", # name
                                "C",  # avatar
                                0, 0  # position
    ))
    g.world.w1 = w1
    g.world.w2 = w2
    g.iteration = i
    g.wins = num_win

    # Run!
    g.go(1)
    win = "me found the exit"
    if g.world.events:
        if win == str(g.world.events[0]):
            num_win += 1
    
    w1 = g.world.w1
    w2 = g.world.w2

print((w1, w2))
print(num_win)
