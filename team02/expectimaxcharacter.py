# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from events import Event
import math

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        char = next(iter(wrld.characters.values()))[0]
        mons = next(iter(wrld.monsters.values()))[0]
        ex = wrld.exitcell

        # Character has index 0 and monsters have index >= 1
        def getLegalActions(charIndex, wrld):
            legalActions = []

            if charIndex == 0: 
                e = char
            else:
                e = mons

            # Go through the possible 8-moves of the entity
            for dx in [-1, 0, 1]:
                # Avoid out-of-bound indexing
                if (e.x + dx >= 0) and (e.x + dx < wrld.width()):
                    # Loop through delta y
                    for dy in [-1, 0, 1]:
                        # Make sure the monster is moving
                        if (dx != 0) or (dy != 0):
                            # Avoid out-of-bound indexing
                            if (e.y + dy >= 0) and (e.y + dy < wrld.height()):
                                # No need to check impossible moves
                                if not wrld.wall_at(e.x + dx, e.y + dy):
                                    if charIndex == 0:
                                        if not wrld.monsters_at(e.x + dx, e.y + dy):
                                            legalActions.append([dx, dy])
                                    else:
                                        legalActions.append((dx, dy))

            return legalActions

        def max_value(depth, world, events):
            for event in events:
                print(event)
                if event.tpe == 2 or event.tpe == 3:
                    print("DIE")
                    return world.scores[char.name] - 100000000000
                elif event.tpe == 4:
                    return world.scores[char.name] + 1000000
                   
            char_max = next(iter(world.characters.values()))[0]
            distance = math.dist([char_max.x, char_max.y], [ex[0], ex[1]] )

            if depth == 3:
                return world.scores[char_max.name]- distance

            v = float("-inf")
            for a in getLegalActions(0, world):
                char.move(a[0], a[1])
                (newwrld, newevents) = world.next()
                v = max(v, exp_value(depth + 1, newwrld, newevents))
            return v

        def exp_value(depth, world, events):
            for event in events:
                print(event)
                if event.tpe == 2 or event.tpe == 3:
                    print("NICE")
                    return world.scores[char.name] - 100000000000
                elif event.tpe == 4:
                    return world.scores[char.name] + 1000000

            mons_exp = next(iter(world.monsters.values()))[0]
            char_exp = next(iter(world.characters.values()))[0]
            distance = math.dist([char_exp.x, char_exp.y], [ex[0], ex[1]] )            

            if depth == 3:
                return world.scores[char_exp.name] - distance                

            v = 0
            p = 1.0 / len(getLegalActions(1, world)) * 10
            for a in getLegalActions(1, world):
                mons_exp.move(a[0], a[1])
                (newwrld, newevents) = world.next()
                v = v + p * max_value(depth + 1, newwrld, newevents)
            return v

        maximum = float("-inf")
        action = (0, 0)
        for a in getLegalActions(0, wrld):
            print(a)
            char.move(a[0], a[1])
            (newwrld,events) = wrld.next()
            utility = exp_value(0, newwrld, events)
            print(utility)
            if utility >= maximum or maximum == float("-inf"):
                maximum = utility
                action = a

        self.move(action[0], action[1])
