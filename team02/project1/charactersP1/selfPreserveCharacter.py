# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import search

class SelfPreserveCharacter(CharacterEntity):

    def do(self, wrld):
        
        # Check monster location
        is_monster_near = self.monster_nearby(wrld, 5)
        path = search.astar(self, wrld)
        monst = next(iter(wrld.monsters.values()))[0]
        monstPath = search.astar(monst, wrld)
        
        # We will always get ahead of the monster, so we might aswell bypass all
        if len(path) < len(monstPath) - 1:
            walk = path.pop(0)
            self.move(walk[0] - self.x, walk[1] - self.y)
        
        # Use Astar to go to goal while not near a monster
        elif is_monster_near != True:
            walk = path.pop(0)
            self.move(walk[0] - self.x, walk[1] - self.y)
        
        # We go to the goal if we are right there
        elif search.euclidean((self.x, self.y), wrld.exitcell) < 2:
            self.move(wrld.exitcell[0] - self.x, wrld.exitcell[1] - self.y)
       
        # Flip to minimax while near a monster
        else:
            walk = self.minimax(wrld, 3)
            self.move(walk[0], walk[1])

    def monster_nearby(self, wrld, near):
        '''
        :param wrld          [SensedWorld]   Our world
        :param near          [int]           How close monster is
        :return monst_exists [bool]          True if we saw a monster
        '''
        monst = next(iter(wrld.monsters.values()))[0]
        if search.euclidean((self.x, self.y), (monst.x, monst.y)) < near:
            return True
        else:
            return False

    def minimax(self, wrld, depth):
        '''
        Our minimax algorithm for the AI of the Bomberman
        :param wrld         [SensedWorld]   Our world
        :param depth        [int]           How far we want to look
        :return (dx, dy)    [(int, int)]    The change in where we want to move to
        '''
        path = []
        path_list = []
        curr_depth = 0
        alpha = -1000
        beta = 1000

        newwrld = wrld.from_world(wrld)
        
        # these work well.
        char = next(iter(newwrld.characters.values()))[0]
        monst = next(iter(newwrld.monsters.values()))[0]
        
        # Assign utility for first max function that follows
        u = -1000

        # We check the bombermans moves at this stage
        for dx in [-1, 0, 1]:
            if char.x + dx >= 0 and char.x + dx < wrld.width():
                for dy in [-1, 0, 1]:
                    if (dx != 0 or dy != 0) and char.y + dy >= 0 and char.y + dy < wrld.height():
                        if not wrld.wall_at(char.x + dx, char.y + dy):
                            # Character moves, and all events happen, now we move forward with the code
                            char.move(dx, dy)
                            (newerwrld, events) = newwrld.next()

                            # No events happened
                            if len(events) == 0:
                                try:
                                    newchar, newmonst = SelfPreserveCharacter.get_char_and_monst(newerwrld)
                                except:
                                    print("why?")
                                    continue

                                # Absolutely never get close to the monster
                                dist_to_monst = search.euclidean((newchar.x, newchar.y), (newmonst.x, newmonst.y))
                                if dist_to_monst < 1.5:
                                    u = -90
                                else:
                                    u, alpha, beta = SelfPreserveCharacter.min_val(newwrld, depth, curr_depth, newchar, newmonst, alpha, beta)

                                # We get our path from the previous values.
                                path = (u, (dx, dy))
                                path_list.append(path)

                            # Terminal, we got killed by a monster
                            elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER:
                                events = []
                                print("murder")
                                u = -100
                                path = (u, (dx, dy))
                                path_list.append(path)
                                continue

                            # Terminal, we found the exit
                            elif events[0].tpe == events[0].CHARACTER_FOUND_EXIT:
                                print("EXIT FOUND")
                                events = []
                                return (dx, dy) # immediately give path to goal
                           

        # get our best path, and assign it in a way we will use for movement later
        best_path = max(path_list)
        (util, path) = best_path
        
        return path

    @staticmethod
    def max_val(wrld, depth, curr_depth, char, monst, a, b):
        '''
        Calculating what Bomberman will do
        :param wrld         [SensedWorld]   Our world
        :param depth        [int]           Depth we want to reach
        :param curr_depth   [int]           Current Depth
        :param char         [Character]     Current Character
        :param monst        [Monster]       First Monster
        :param a            [float]         Alpha for alpha beta pruning
        :param b            [float]         Beta for alpha beta pruning

        :return [float] utility value
        '''
        curr_depth += 1
        u_new = -100

        # set u for max
        u = -100
        
        # We check the bombermans moves at this stage
        for dx in [-1, 0, 1]:
            if char.x + dx >= 0 and char.x + dx < wrld.width():
                for dy in [-1, 0, 1]:
                    if (dx != 0 or dy != 0) and char.y + dy >= 0 and char.y + dy < wrld.height():
                        if not wrld.wall_at(char.x + dx, char.y + dy):
                            # All bomberman actions and moves getting played:
                            char.move(dx, dy)
                            (newwrld, events) = wrld.next()
                            

                            # No events happened during move:
                            if len(events) == 0:
                                try:
                                    newchar, newmonst = SelfPreserveCharacter.get_char_and_monst(newwrld)
                                except:
                                    continue
                                
                                # If we are at depth, assign value:
                                if curr_depth == depth:
                                    u = max(u, SelfPreserveCharacter.reward(newchar, newmonst, newwrld, True))

                                    if u >= b:
                                        return u, a, b

                                    a = max(a, u)

                                # If we aren't at depth, go deeper:
                                else:
                                    u_new, a, b = SelfPreserveCharacter.min_val(newwrld, depth, curr_depth, newchar, newmonst, a, b)
                                    u = max(u, u_new)                
                                    
                            
                            # Terminal, character killed
                            elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER:
                                u = max(u, -100)
                                continue

                            # Terminal, character found exit
                            elif events[0].tpe == events[0].CHARACTER_FOUND_EXIT:
                                u = 100
                                return u, a, b # immediately return, can't get better
        return u, a, b

    @staticmethod
    def min_val(wrld, depth, curr_depth, char, monst, a, b):
        '''
        Calculating what Monster will do
        :param wrld         [SensedWorld]   Our world
        :param depth        [int]           Depth we want to reach
        :param curr_depth   [int]           Current Depth
        :param char         [Character]     Current Character
        :param monst        [Monster]       First Monster
        :param a            [float]         Alpha for alpha beta pruning
        :param b            [float]         Beta for alpha beta pruning

        :return [float] utility value
        '''
        curr_depth += 1
        u_new = 100

        # set u for min
        u = 100
        
        # We check the monsters moves at this stage
        for dx in [-1, 0, 1]:
            if monst.x + dx >= 0 and monst.x + dx < wrld.width():
                for dy in [-1, 0, 1]:
                    if (dx != 0 or dy != 0) and monst.y + dy >= 0 and monst.y + dy < wrld.height():
                        if not wrld.wall_at(monst.x + dx, monst.y + dy):
                            monst.move(dx, dy)
                            (newwrld, events) = wrld.next()

                            # No events
                            if len(events) == 0:
                                try:
                                    newchar, newmonst = SelfPreserveCharacter.get_char_and_monst(newwrld)
                                except:
                                    continue
                                
                                # reached max depth
                                if curr_depth == depth:
                                    u = min(u, SelfPreserveCharacter.reward(newchar, newmonst, newwrld))
                                    
                                    if u <= a:
                                        return u, a, b

                                    b = min(b, u)

                                # not at max depth, go deeper
                                else:
                                    u_new, a, b = SelfPreserveCharacter.max_val(newwrld, depth, curr_depth, newchar, newmonst, a, b)
                                    u = min(u, u_new)

                            # Terminal, character killed
                            elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER:
                                u = -100
                                return u, a, b
                                

        return u, a, b


    @staticmethod
    def reward(char, monst, wrld, Player = False):
        '''
        We are calculating the reward of where we end with in the algorithm
        :param char     [Character]     our current character
        :param monst    [Monster]       our first monster
        :param wrld     [SensedWorld]   our world

        :return R       [Float]         reward value
        '''
        R = 0
        # distance to goal
        goal = wrld.exitcell
        g_weight = 0.5

        a_path = search.astar(char, wrld)

        R -= len(a_path)*g_weight
        
        dist_to_monst = search.euclidean((char.x, char.y), (monst.x, monst.y))

        if dist_to_monst < 1.5 and Player == False:
            R -= 20
        elif dist_to_monst < 1.5 and Player:
            R -= -80
        elif dist_to_monst < 3:
            R -= 5
        elif dist_to_monst < 5.2:
            R -= 3
        elif dist_to_monst < 7:
            R -= 1
        
        return R

    @staticmethod
    def get_char_and_monst(wrld):
        '''
        We are getting our characters
        :param wrld     [SensedWorld]   our world

        :return char    [Character]
        :return monster [Monster]
        '''
        char = next(iter(wrld.characters.values()))[0]
        monst = next(iter(wrld.monsters.values()))[0]
        return char, monst
        
        
