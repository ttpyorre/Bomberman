# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from events import Event
from colorama import Fore, Back
import search

class MinimaxCharacter(CharacterEntity):

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
        # for dx in [-1, 0, 1]:
        #     if char.x + dx >= 0 and char.x + dx < wrld.width():
        #         for dy in [-1, 0, 1]:
        #             if (dx != 0 or dy != 0) and char.y + dy >= 0 and char.y + dy < wrld.height():
        #                 if not wrld.wall_at(char.x + dx, char.y + dy):

        actions = self.get_char_available_actions(wrld, char.x, char.y)

        for (dx, dy, use_bomb) in actions:
            # Character moves, and all events happen, now we move forward with the code

            if use_bomb:
                char.place_bomb()

            char.move(dx, dy)
            (newerwrld, events) = newwrld.next()

            # No events happened
            if len(events) == 0:
                try:
                    newchar, newmonst = MinimaxCharacter.get_char_and_monst(newerwrld)
                except:
                    print("why?")
                    continue

                # Absolutely never get close to the monster
                dist_to_monst = search.euclidean((newchar.x, newchar.y), (newmonst.x, newmonst.y))
                if dist_to_monst < 1.5:
                    u = -90
                else:
                    u, alpha, beta = self.min_val(newwrld, depth, curr_depth, newchar, newmonst, alpha, beta)

                # We get our path from the previous values.
                path = (u, (dx, dy))
                path_list.append(path)

            # Terminal, we got killed by a monster
            elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER or events[0].tpe == events[0].BOMB_HIT_CHARACTER:
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

            # elif events[0].tpe == events[0].BOMB_HIT_WALL:
            # elif events[0].tpe == events[0].BOMB_HIT_MONSTER :


        # get our best path, and assign it in a way we will use for movement later
        best_path = max(path_list)
        (util, path) = best_path
        
        return path

        
    @staticmethod
    def get_char_available_actions(wrld, x, y):
        """
        Gets the available moves at position x, y, and us of bombs
            Note, only checks for walls, or out of bounds
        """ 

        # check to see if a bomb exist

        bomb_exist = False

        try:
            bomb = next(iter(wrld.bombs.values()))[0]
            bomb_exist = True
        except:
            print("no bombs exist")
        
        actions = []

        for dx in [-1, 0, 1]:
            if x + dx >= 0 and x + dx < wrld.width():
                for dy in [-1, 0, 1]:
                    if (dx != 0 or dy != 0) and y + dy >= 0 and y + dy < wrld.height():
                        if not wrld.wall_at(x + dx, y + dy):

                            # add as a possible action to place a bomb and move
                            # regardless of the situation, we should be allowed to move without placing a bomb
                            actions.append((dx, dy, False))

                            if not bomb_exist:
                                # give myself the option to place a bomb
                                actions.append((dx, dy, True))

        return actions



    @staticmethod
    def get_available_actions(wrld, x, y):
        """
        Gets the available moves at position x, y
            Note, only checks for walls, or out of bounds
        """ 
        
        actions = []

        for dx in [-1, 0, 1]:
            if x + dx >= 0 and x + dx < wrld.width():
                for dy in [-1, 0, 1]:
                    if (dx != 0 or dy != 0) and y + dy >= 0 and y + dy < wrld.height():
                        if not wrld.wall_at(x + dx, y + dy):

                            # if not out of bounds or wall present at that location
                            # add the move
                            actions.append((dx, dy))

        return actions

    def max_val(self, wrld, depth, curr_depth, char, monst, a, b):
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

        actions = self.get_char_available_actions(wrld, char.x, char.y)

        for (dx, dy, use_bomb) in actions:

            print((dx, dy, use_bomb))

            (newwrld, events) = (None, None)

            if use_bomb:
                char.place_bomb()
                char.move(dx, dy)
                (newwrld, events) = wrld.next()
                newwrld.printit()
            else:
                char.move(dx, dy)
                (newwrld, events) = wrld.next()

            murder = False
            exit_found = False
            for event in events:
                if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER: murder = True
                if event.tpe == Event.BOMB_HIT_CHARACTER: murder = True
                if event.tpe == Event.CHARACTER_FOUND_EXIT: exit_found = True
                break

            if murder:
                # Terminal, character killed
                u = -100
                return u, a, b
            
            # Terminal, character killed
            if murder:
                u = max(u, -100)
                continue
            # Terminal, character found exit
            elif exit_found:
                u = 100
                return u, a, b # immediately return, can't get better
            else:
                try:
                    newchar, newmonst = MinimaxCharacter.get_char_and_monst(newwrld)
                except:
                    continue
                
                # If we are at depth, assign value:
                if curr_depth == depth:
                    u = max(u, MinimaxCharacter.reward(newchar, newmonst, newwrld, events, True))

                    if u >= b:
                        return u, a, b

                    a = max(a, u)

                # If we aren't at depth, go deeper:
                else:
                    u_new, a, b = self.min_val(newwrld, depth, curr_depth, newchar, newmonst, a, b)
                    u = max(u, u_new)                
                    
            
            # # Terminal, character killed
            # elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER:
            #     u = max(u, -100)
            #     continue

            # # Terminal, character found exit
            # elif events[0].tpe == events[0].CHARACTER_FOUND_EXIT:
            #     u = 100
            #     return u, a, b # immediately return, can't get better
        return u, a, b

    
    def min_val(self, wrld, depth, curr_depth, char, monst, a, b):
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

        actions = self.get_available_actions(wrld, monst.x, monst.y)

        for (dx, dy) in actions:

            monst.move(dx, dy)

            (newwrld, events) = wrld.next()

            murder = False
            for event in events:
                if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER: murder = True
                if event.tpe == Event.BOMB_HIT_CHARACTER: murder = True
                break

            if murder:
                # Terminal, character killed
                u = -100
                return u, a, b

            # No events
            else:
                try:
                    newchar, newmonst = MinimaxCharacter.get_char_and_monst(newwrld)
                except:
                    continue
                
                # reached max depth
                if curr_depth == depth:
                    u = min(u, MinimaxCharacter.reward(newchar, newmonst, newwrld, events))
                    
                    if u <= a:
                        return u, a, b

                    b = min(b, u)

                # not at max depth, go deeper
                else:
                    u_new, a, b = self.max_val(newwrld, depth, curr_depth, newchar, newmonst, a, b)
                    u = min(u, u_new)

            
            # elif events[0].tpe == events[0].CHARACTER_KILLED_BY_MONSTER:
            #     u = -100
            #     return u, a, b
                                
        return u, a, b


    @staticmethod
    def reward(char, monst, wrld, events, Player = False):
        '''
        We are calculating the reward of where we end with in the algorithm
        :param char     [Character]     our current character
        :param monst    [Monster]       our first monster
        :param wrld     [SensedWorld]   our world

        :return R       [Float]         reward value
        '''
        R = 0

        for event in events:
            if event.tpe == Event.BOMB_HIT_MONSTER: R += 50
            if event.tpe == Event.BOMB_HIT_WALL: R += 10

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
        
        
