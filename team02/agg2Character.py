# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import search

class AggCharacter(CharacterEntity):

    def do(self, wrld):
        
        # Check monster location
        is_monster_near = self.monster_nearby(wrld, 5)
        
        # Use Astar to go to goal while not near a monster
        if is_monster_near != True:
            path = search.astar(self, wrld)
            walk = path.pop(0)
            self.move(walk[0] - self.x, walk[1] - self.y)
        
        # We go to the goal if we are right there
        elif search.euclidean((self.x, self.y), wrld.exitcell) < 2:
            self.move(wrld.exitcell[0] - self.x, wrld.exitcell[1] - self.y)
        
        # Flip to minimax while near a monster
        else:
            walk = self.minimax(wrld, 4)
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
        :param wrld
        :param depth
        :return location we should move to
        '''
        path = []
        path_list = []
        curr_depth = 0
        alpha = -1000
        beta = 1000

        newwrld = wrld.from_world(wrld)
        
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
                            # Check terminal states
                            


                            # No events happened
                            if len(events) == 0:
                                u, alpha, beta = AggCharacter.min_val(newwrld, depth, curr_depth, char, monst, alpha, beta)

                                print(beta)
                                print(alpha)
                                # We get our path from the previous values.
                                path = (u, (dx, dy))
                                print(path)
                                path_list.append(path)

                            # Terminal, we got killed by a monster
                            elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER:
                                u = -100
                                path = (u, (dx, dy))
                                path_list.append(path)
                                continue

                            # Terminal, we found the exit
                            elif events[0].tpe == events[0].CHARACTER_FOUND_EXIT:
                                return (dx, dy) # immediately give path to goal
                           

        # get our best path, and assign it in a way we will use for movement later
        best_path = max(path_list)
        (util, path) = best_path
        
        return path

    @staticmethod
    def max_val(wrld, depth, curr_depth, char, monst, a, b):
        '''
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
                            
                            char, monst, newwrld = AggCharacter.get_char_and_monst(newwrld, char, monst)

                            # No events happened during move:
                            if len(events) == 0:
                                
                                # If we are at depth, assign value:
                                if curr_depth == depth:
                                    u = max(u, AggCharacter.reward(char, monst, newwrld))

                                    if u >= b:
                                        return u, a, b

                                    a = max(a, u)

                                # If we aren't at depth, go deeper:
                                else:
                                    u_new, a, b = AggCharacter.min_val(newwrld, depth, curr_depth, char, monst, a, b)
                                    u = max(u, u_new)                
                                    
                            
                            # Terminal, character killed
                            elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER:
                                u = max(u, -100)
                                continue

                            # Terminal, character found exit
                            elif events[0].tpe == events[0].CHARACTER_FOUND_EXIT:
                                print("we found exit?")
                                u = 100
                                return u, a, b # immediately return, can't get better
        return u, a, b

    @staticmethod
    def min_val(wrld, depth, curr_depth, char, monst, a, b):
        '''
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
                            
                            char, monst, newwrld = AggCharacter.get_char_and_monst(newwrld, char, monst)

                            # No events
                            if len(events) == 0:
                                
                                # reached max depth
                                if curr_depth == depth:
                                    u = min(u, AggCharacter.reward(char, monst, newwrld))
                                    
                                    '''
                                    if u <= a:
                                        return u, a, b

                                    b = min(b, u)
                                    '''

                                # not at max depth, go deeper
                                else:
                                    u_new, a, b = AggCharacter.max_val(newwrld, depth, curr_depth, char, monst, a, b)
                                    u = min(u, u_new)

                            # Terminal, character killed
                            elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER:
                                u = -100
                                return u, a, b
                                

        return u, a, b


    @staticmethod
    def reward(char, monst, wrld):
        '''
        '''
        R = 0
        # distance to goal
        goal = wrld.exitcell
        g_weight = 0.8

        a_path = search.astar(char, wrld)

        R -= len(a_path)*g_weight
        
        dist_to_monst = search.euclidean((char.x, char.y), (monst.x, monst.y))

        if dist_to_monst < 1.5:
            R -= 1.5
        elif dist_to_monst < 3:
            R -= 1
        elif dist_to_monst < 4:
            R -= 0.5
        
        return R

    @staticmethod
    def terminal_states(wrld, char, monst):
        
        if 
        
