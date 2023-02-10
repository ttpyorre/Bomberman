
# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import search

class BugTestVar5(CharacterEntity):

    def do(self, wrld):
        
        # getting monsters
        monstKey, monst2Key = wrld.monsters.keys()
        monst = wrld.monsters[monstKey][0]
        monst2 = wrld.monsters[monst2Key][0]

        print("---------------------------")
        print("Monster 1 position:")
        print((monst.x, monst.y))
        print("Monster 2 position:")
        print((monst2.x, monst2.y))
        print("Character position:")
        print((self.x, self.y))

        if self.x < 2:
            self.move(1, 0)
        else:
            self.move(-1, 0)

