# This is/  project1 necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class InteractiveCharacterBugSearch(CharacterEntity):

    def do(self, wrld):
        # Commands
        dx, dy = 0, 0
        bomb = False
        self.move_simulation(wrld)
        # Handle input
        for c in input("How would you like to move (w=up,a=left,s=down,d=right,b=bomb)? "):
            if 'w' == c:
                dy -= 1
            if 'a' == c:
                dx -= 1
            if 's' == c:
                dy += 1
            if 'd' == c:
                dx += 1
            if 'b' == c:
                bomb = True
        # Execute commands
        self.move(dx, dy)
        if bomb:
            self.place_bomb()

    def move_simulation(self, wrld):
        '''
        Simulating our movement
        '''
        # Make our new world
        newwrld = wrld.from_world(wrld)
        
        # these work well.
        char = next(iter(newwrld.characters.values()))[0]
        monst = next(iter(newwrld.monsters.values()))[0]
        
        # We check the bombermans moves at this stage
        for dx in [-1, 0, 1]:
            if char.x + dx >= 0 and char.x + dx < wrld.width():
                for dy in [-1, 0, 1]:
                    if char.y + dy >= 0 and char.y + dy < wrld.height():
                        if not wrld.wall_at(char.x + dx, char.y + dy):
                            # Character moves, and all events happen, now we move forward with the code
                            char.move(dx, dy)
                            (newerwrld, events) = newwrld.next()

                            if len(events) == 0:
                                print("yeey! no events :)")

                            elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER:
                                print("-------------------------------------")
                                print("I want to move:")
                                print((dx, dy))
                                print("But, I died.")

