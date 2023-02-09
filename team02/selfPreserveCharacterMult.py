# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import search

class SelfPreserveCharacterMult(CharacterEntity):

    def do(self, wrld):
        # Check monster location
        path = search.astar(self, wrld)
        
        # Getting the monsters
        try:
            are_monsters_near = self.monsters_nearby(wrld, 4)
            monstKey, monst2Key = wrld.monsters.keys()
            monst = wrld.monsters[monstKey][0]
            monst2 = wrld.monsters[monst2Key][0]
            monstPath = search.astar(monst, wrld)
            monstPath2 = search.astar(monst2, wrld)
        except:
            monstPath = []
            monstPath2 = []
            are_monsters_near = False
        
        # We will always get ahead of the monster, so we might aswell bypass all
        if (len(path) < len(monstPath) - 1 and len(path) < len(monstPath2) - 1):
            walk = path.pop(0)
            self.move(walk[0] - self.x, walk[1] - self.y)
        
        # Use Astar to go to goal while not near a monster
        elif are_monsters_near != True:
            walk = path.pop(0)
            self.move(walk[0] - self.x, walk[1] - self.y)
        
        # We go to the goal if we are right there
        elif search.euclidean((self.x, self.y), wrld.exitcell) < 2:
            self.move(wrld.exitcell[0] - self.x, wrld.exitcell[1] - self.y)
       
        # Flip to minimax while near a monster
        else:
            walk = self.minimax(wrld, 2)
            self.move(walk[0], walk[1])

    def monsters_nearby(self, wrld, near):
        '''
        Check if either monster exists around us
        :param wrld          [SensedWorld]   Our world
        :param near          [int]           How close monster is
        :return monst_exists [bool]          True if we saw a monster
        '''
        # get all monsters
        monstKey, monst2Key = wrld.monsters.keys()
        monst = wrld.monsters[monstKey][0]
        monst2 = wrld.monsters[monst2Key][0]
    
        # Either monster nearby would be deadly for us.
        if search.euclidean((self.x, self.y), (monst.x, monst.y)) < near or search.euclidean((self.x, self.y), (monst2.x, monst2.y)) < near:
            return True
        else:
            return False

    def minimax(self, wrld, depth):
        '''
        Minimax algorithm for going past the two monsters
        :param wrld     [SensedWorld]   our world
        :param depth    [int]           the depth we want to go to
        :return location we should move to
        '''
        path = []
        path_list = []
        curr_depth = 0
        alpha = -1000
        beta = 1000

        newwrld = wrld.from_world(wrld)
        
        # these work well.
        char = next(iter(newwrld.characters.values()))[0]
        monstKey, monst2Key = wrld.monsters.keys()
        monst = wrld.monsters[monstKey][0]
        monst2 = wrld.monsters[monst2Key][0]
        
        # Assign utility for first max function that follows
        u = -1000

        # We check the bombermans moves at this stage
        for dx in [-1, 0, 1]:
            if char.x + dx >= 0 and char.x + dx < wrld.width():
                for dy in [-1, 0, 1]:
                    if char.y + dy >= 0 and char.y + dy < wrld.height():
                        if not wrld.wall_at(char.x + dx, char.y + dy):
                            # Character moves, and all events happen, now we move forward with the code
                            char.move(dx, dy)
                            (newerwrld, events) = newwrld.next()

                            # No events happened
                            if len(events) == 0:
                                try:
                                    newchar, newmonst, newmonst2 = SelfPreserveCharacterMult.get_char_and_monst(newerwrld)
                                except:
                                    continue
                                
                                monst_dist = search.euclidean((newchar.x, newchar.y), (newmonst.x, newmonst.y))
                                monst_dist2 = search.euclidean((newchar.x, newchar.y), (newmonst2.x, newmonst2.y))
                                if monst_dist < 2.8:
                                    u = -1000 + monst_dist + monst_dist2*0.2
                                elif monst_dist2 < 2.8:
                                    u = -1000 + monst_dist2
                                else:
                                    u = SelfPreserveCharacterMult.min_val(newwrld, depth, curr_depth, newchar, newmonst, newmonst2, alpha, beta)

                                # We get our path from the previous values.
                                path = (u, (dx, dy))
                                print(path)
                                path_list.append(path)

                            # Terminal, we got killed by a monster
                            elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER:
                                u = -10000
                                path = (u, (dx, dy))
                                path_list.append(path)
                                continue

                            # Terminal, we found the exit
                            elif events[0].tpe == events[0].CHARACTER_FOUND_EXIT:
                                print("EXIT FOUND")
                                return (dx, dy) # immediately give path to goal
                           

        # get our best path, and assign it in a way we will use for movement later
        best_path = max(path_list)
        (util, path) = best_path
        
        return path

    @staticmethod
    def max_val(wrld, depth, curr_depth, char, monst, monst2, a, b):
        '''
        Calculating what Bomberman will do
        :param wrld         [SensedWorld]   Our world
        :param depth        [int]           Depth we want to reach
        :param curr_depth   [int]           Current Depth
        :param char         [Character]     Current Character
        :param monst        [Monster]       First Monster
        :param monst2       [Monster]       Second Monster
        :param a            [float]         Alpha for alpha beta pruning
        :param b            [float]         Beta for alpha beta pruning

        :return [float] utility value
        '''
        curr_depth += 1

        # set u for max
        u = -100000
        
        # We check the bombermans moves at this stage
        for dx in [-1, 0, 1]:
            if char.x + dx >= 0 and char.x + dx < wrld.width():
                for dy in [-1, 0, 1]:
                    if char.y + dy >= 0 and char.y + dy < wrld.height():
                        if not wrld.wall_at(char.x + dx, char.y + dy):
                            # All bomberman actions and moves getting played:
                            char.move(dx, dy)
                            (newwrld, events) = wrld.next()
                            

                            # No events happened during move:
                            if len(events) == 0:
                                try:
                                    newchar, newmonst, newmonst2 = SelfPreserveCharacterMult.get_char_and_monst(newwrld)
                                except:
                                    continue
                                
                                # If we are at depth, assign value:
                                if curr_depth == depth:
                                    u = max(u, SelfPreserveCharacterMult.reward(newchar, newmonst, newmonst2, newwrld, True))

                                    if u >= b:
                                        return u

                                # If we aren't at depth, go deeper:
                                else:
                                    u_new = SelfPreserveCharacterMult.min_val(newwrld, depth, curr_depth, newchar, newmonst, newmonst2, a, b)
                                   
                                    if u_new >= b:
                                        return u_new
                                    
                                    u = max(u, u_new)
                                    a = max(a, u)
                                    
                            
                            # Terminal, character killed
                            elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER:
                                u = -1000
                                return u

                            # Terminal, character found exit
                            elif events[0].tpe == events[0].CHARACTER_FOUND_EXIT:
                                u = 1000
                                return u # immediately return, can't get better
        return u

    @staticmethod
    def min_val(wrld, depth, curr_depth, char, monst, monst2, a, b):
        '''
        Calculating what our first monster will do
        :param wrld         [SensedWorld]   Our world
        :param depth        [int]           Depth we want to reach
        :param curr_depth   [int]           Current Depth
        :param char         [Character]     Current Character
        :param monst        [Monster]       First Monster
        :param monst2       [Monster]       Second Monster
        :param a            [float]         Alpha for alpha beta pruning
        :param b            [float]         Beta for alpha beta pruning

        :return [float] utility value
        '''
        # set u for min
        u = 100000
        
        # We check the monsters moves at this stage
        for dx in [-1, 0, 1]:
            if monst.x + dx >= 0 and monst.x + dx < wrld.width():
                for dy in [-1, 0, 1]:
                    if (dx != 0 or dy != 0) and monst.y + dy >= 0 and monst.y + dy < wrld.height():
                        if not wrld.wall_at(monst.x + dx, monst.y + dy) or wrld.monsters_at(monst.x + dx, monst.y + dy):
                            monst.move(dx, dy)
                            (newwrld, events) = wrld.next()

                            # No events
                            if len(events) == 0:
                                try:
                                    newchar, newmonst, newmonst2 = SelfPreserveCharacterMult.get_char_and_monst(newwrld)
                                except:
                                    continue 

                                # reached max depth
                                if curr_depth == depth:
                                    u = min(u, SelfPreserveCharacterMult.reward(newchar, newmonst, newmonst2, newwrld))
                                    
                                    if u <= a:
                                        return u

                                # not at max depth, go deeper
                                else:
                                    u_new = SelfPreserveCharacterMult.min_val2(newwrld, depth, curr_depth, newchar, newmonst, newmonst2, a, b)
                                    
                                    if u_new < a:
                                        return u_new
                                    
                                    u = min(u, u_new)
                                    b = min(b, u)

                            # Terminal, character killed
                            elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER:
                                u = -100000
                                return u

        return u

    @staticmethod
    def min_val2(wrld, depth, curr_depth, char, monst, monst2, a, b):
        '''
        Calculating what our first monster will do
        :param wrld         [SensedWorld]   Our world
        :param depth        [int]           Depth we want to reach
        :param curr_depth   [int]           Current Depth
        :param char         [Character]     Current Character
        :param monst        [Monster]       First Monster
        :param monst2       [Monster]       Second Monster
        :param a            [float]         Alpha for alpha beta pruning
        :param b            [float]         Beta for alpha beta pruning

        :return [float] utility value
        '''
        # set u for min
        u = 10000
        curr_depth += 1
        
        # We check the second monsters moves at this stage
        for dx in [-1, 0, 1]:
            if monst2.x + dx >= 0 and monst2.x + dx < wrld.width():
                for dy in [-1, 0, 1]:
                    if (dx != 0 or dy != 0) and monst2.y + dy >= 0 and monst2.y + dy < wrld.height():
                        if not (wrld.wall_at(monst2.x + dx, monst2.y + dy) or wrld.monsters_at(monst2.x + dx, monst2.y + dy)):
                            monst2.move(dx, dy)
                            (newwrld, events) = wrld.next()

                            # No events
                            if len(events) == 0:
                                try:
                                    newchar, newmonst, newmonst2 = SelfPreserveCharacterMult.get_char_and_monst(newwrld)
                                except:
                                    continue
                               
                                # reached max depth
                                if curr_depth == depth:
                                    u = min(u, SelfPreserveCharacterMult.reward(newchar, newmonst, newmonst2, newwrld))
                                    
                                    if u <= a:
                                        return u

                                # not at max depth, go deeper
                                else:
                                    u_new = SelfPreserveCharacterMult.max_val(newwrld, depth, curr_depth, newchar, newmonst, newmonst2, a, b)

                                    if u_new < a:
                                        return u_new
                                    
                                    u = min(u, u_new)
                                    b = min(b, u)

                            # Terminal, character killed
                            elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER:
                                u = -1000
                                return u

        return u


    @staticmethod
    def reward(char, monst, monst2, wrld, Player = False):
        '''
        We are calculating the reward of where we end with in the algorithm
        :param char, our current character
        :param monst, our first monster
        :param monst2, our second monster
        :param wrl, our world
        :param Player, boolean to check if we are the player or not

        :return R, reward value
        '''
        R = 0
        # distance to goal
        goal = wrld.exitcell
        g_weight = 0.5

        a_path = search.astar(char, wrld)

        R -= len(a_path)*g_weight
        
        dist_to_monst = search.euclidean((char.x, char.y), (monst.x, monst.y))
        dist_to_monst2 = search.euclidean((char.x, char.y), (monst2.x, monst2.y))

        if dist_to_monst < 1.5 and Player == False:
            R -= 40
        elif dist_to_monst < 1.5 and Player:
            R -= 80
        elif dist_to_monst < 3:
            R -= 30
        
        if dist_to_monst2 < 1.5 and Player == False:
            R -= 40
        elif dist_to_monst2 < 1.5 and Player:
            R -= 80
        elif dist_to_monst2 < 3:
            R -= 30

        return R

    @staticmethod
    def get_char_and_monst(wrld):
        '''
        :param wrld [SensedWorld] our world

        :return char    [Character] our character
        :return monst   [Monster]   our first monster
        :return monst2  [Monster]   our second monster
        '''
        char = next(iter(wrld.characters.values()))[0]
        monstKey, monst2Key = wrld.monsters.keys()
        monst = wrld.monsters[monstKey][0]
        monst2 = wrld.monsters[monst2Key][0]
        return char, monst, monst2
        
        
