# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):
    EXPLORING = 0
    EXPLORE_WALL = 1
    BOMBING = 2
    WAITING = 3
    KEEPWAITING = 4
    RUNNING = 5

    def do(self, wrld, state):  
        print(state)      
        if state == 0:
            self.move(0, 1)
            print("fuck")
            return 2
        elif state == 2:
            self.place_bomb()
            self.move(0, 0)
            # print(3)
            return 3
        elif state == 3:
            self.move(1, -1)
            # print(1)
            return 4
        elif state == 4:
            self.move(0, 0)
            return 5
        elif state == 5:
            self.move(0, 0)
            return 1
        elif state == 1:
            self.move(-1, 1)
            print("fuck2")
            # print(0)
            return 0
        else:
            print("fuck")
            self.move(0, 0)
        
