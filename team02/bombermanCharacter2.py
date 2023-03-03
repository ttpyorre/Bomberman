# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

# Import Priority Queue
from priorityQueue import PriorityQueue
import numpy as np
import math
import search
from LookupTable import StateActionLookupTable, NStateActionTable
import bombermanCharacter 
from events import Event



class BombermanCharacter2(CharacterEntity):

    weight = [3.0, 1.0, 1.0]
    previous_action = (0,0,False)


    def do(self, wrld):

        # get the best move from q learning

        # act on the action given by a'
        

        if self.near_exit(wrld):
            # get the cell closes to the exit
            a = self.dir_to_exit(wrld)
            self.move(a[0], a[1])
            # move there
            pass
        else:
            a = self.appozimate_q_learning(wrld)
            print("action:" +str(a))

            self.move(a[0], a[1])
            if a[2]: 
                self.place_bomb()

    def near_exit(self, wrld):
        return search.euclidean((self.x, self.y), wrld.exitcell) == 1.0
    
    def dir_to_exit(self, wrld):
        dx = wrld.exitcell[0] - self.x
        dy = wrld.exitcell[1] - self.y 
        return (dx, dy, False)

    
    def Q_Value(self, s):
        """
        take all the events... find the q value reletive to the furture state, features and weights
        s [wrld] state
        a [(x, y, use_bomb)] the action that we plan to use
        """
        if s == None:
            return 0
        
        f = self.features(s)
        
        return self.weight[0]*f[0] + self.weight[1]*f[1] + self.weight[2]*f[2]
    
    def update_w(self, learning_rate, delta, wrld):
        # calc delta
        # change the weights of the state

        f = self.features(wrld)

        for i in range(len(self.weight)):
            self.weight[i] += learning_rate*delta*f[i]


    
    def maxQ(self, wrld):
        # gets the best state given the actions avaiable for bomberman 

        char = self.get_char(wrld)

        try:
            if char == None:
                return 0.0
        except:
            #  weirdly enough after this i assume that we have a character
            pass

        max_q = float("-inf")

        possible_actions = bombermanCharacter.get_char_available_actions(wrld, char.x, char.y)
        possible_actions.append((0,0, False))
        best_action = None

        print("possible_actions: " + str(possible_actions))

        

        for a in possible_actions:

            # move the character in the direction specified by a
            # NOTE self.move() does not work for moving the character for the sensed world
            
            char.move(a[0], a[1]) 
            if a[2]: # we are placing a bomb
                char.place_bomb()
                
            (newwrld, events) = wrld.next()     

        
            try:
                q = self.Q_Value(newwrld)
            except:
                q = self.reward(events)

            # print("-:" + str((q, a)))
            if q > max_q:   
                max_q = q
                best_action = a


        return (max_q, best_action)
            
    

    def appozimate_q_learning(self, wrld):
        # get all the results,  s' and s
        #   s' can be obtained from looking at the next world state
        #   a' just says given all the available actions for bomber man
        
        # Find delta
        #   dicounting factor - > lamda
        #   lets define the reward based on what will happen next, without doing anything
        discounting = 0.9
        learning_rate = 0.5

        (newwrld,events) = wrld.next()
        reward = self.reward(events)

        (maxQ, best_action) = self.maxQ(newwrld)
        print("Best:" + str((maxQ, best_action)))

        delta = (reward + discounting*maxQ) - self.Q_Value(wrld)

        # Update the weight
        #   wi = wi + alpha * delta * fi(s,a)
        self.update_w(learning_rate, delta, wrld)

        # Do a'
        # Hopefully s' is the result

        return best_action
    
    # def workable_astar(self, wrld):
        

###++++++++++++++++++++Tested - Possible to Chage ++++++++++++++++++++++++++

     
    def features(self, wrld):

        f = []

        char = self.get_char(wrld)

        # feature 1: Dist to exit cell
        
        dist_to_exit = search.euclidean((char.x, char.y), wrld.exitcell)
        # dist_to_exit = len(search.astar(char, wrld, wrld.exitcell))

        f0 = 1.0/(1.0+dist_to_exit) 
        f.append(f0)
        
        # feature 2: Bomb is there a bomb
        f1 = 1.0
        if search.is_bomb_active(wrld):
            f1 = 2.0

        f.append(f1)
        
        # feature 3:
        f2 = 1.0
        f.append(f2)

        return f


###+++++++++++++++++++++++++++++ Tested ++++++++++++++++++++++++++++++++++++##

    
    
    @staticmethod
    def reward(events):

        for event in events:
            if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER: 
                return -10.0
            if event.tpe == Event.BOMB_HIT_CHARACTER: 
                return -20.0
            if event.tpe == Event.BOMB_HIT_WALL:
                return 5.0
            if event.tpe == Event.CHARACTER_FOUND_EXIT: 
                return 10.0
            
        return -1.0

    @staticmethod
    def get_char(wrld):
        try:
            char = next(iter(wrld.characters.values()))[0]
            return char
        except:
            print("Hey, there is no char in world")
            return None

    


