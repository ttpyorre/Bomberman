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

def get_all_possible_actions():
    actions = []

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            actions.append((dx, dy, False))
    return actions


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

    return actions



class BombermanCharacter(CharacterEntity):

    # Defining type sof states for the bomberman
    NORMAL = 0                  # Nothing noticable, normal
    AVOID_BOMB = 1              # 
    WALK_BACK_TO_PATH = 2

    STATE = 1
    save_point = (0 , 0)

    all_states = [1, 2, 3, 4, 5, 6, 7, 8]

    possible_actions = []
    
    previous_state = 1
    previous_action = (0,0,False)  # Do nothing
    reward = 0

    QTable = StateActionLookupTable(all_states, get_all_possible_actions())
    NTable = NStateActionTable(all_states, get_all_possible_actions())

    def do(self, wrld):

        # print(search.get_all_possible_actions())
        # print(self.all_states)

        # print(self.QTable.get(0, (0, 0, False)))

        self.possible_actions = get_char_available_actions(wrld, self.x, self.y)

        if self.previous_state != None: 
            # self.reward = search
            pass

        current_state = self.x + 1
        self.reward = self.reward_calc(self.previous_state, current_state)

        print("prev:" + str(self.previous_state) + "curr:" + str(current_state))
        action = self.q_learning(current_state, self.reward)
        self.execute_action(action[0], action[1], action[2])
        pass

    def execute_action(self, dx, dy, use_bomb):
        self.move(dx, dy)
        if use_bomb: self.place_bomb()

    def q_learning(self, current_state = None, reward = 0):
        """
        current_state   - (s') the current state of the character
        reward          - R(s, a, s') the reward we just got from doing an action
        """
        def get_max_q():
            max_q = None
            for a in self.possible_actions:
                q = self.QTable.get(current_state, a)

                if max_q == None or q > max_q:   
                    max_q = q

            return max_q

        def explore_actions():
            max_value = None
            best_a = None
            for a in self.possible_actions:

                
                value = self.explore(self.QTable.get(current_state, a), self.NTable.get(current_state, a))

                if max_value == None or value > max_value:   
                    max_value = value
                    best_a = a

            return best_a
                
                

        s = self.previous_state
        a = self.previous_action

        alpha = 0.9 # learning rate
        decay = 0.9
        
        if s != None:

            # # Indicate that we tried the state-action
            self.NTable.update(s, a)

            # Update Q(s, a) using s', a' (current), s, a (past)
            n = self.NTable.get(s, a)
            max_q = get_max_q()
            q = self.QTable.get(s, a)

            print("Reward: " + str(reward))
            print(decay*max_q - q)

            value = alpha*n*(reward + decay*max_q - q)
            self.QTable.update(s, a, value)

        # choose the best action (unexplored action or best util)
        best_action = explore_actions()

        # Update previous state and actions
        self.previous_state = current_state
        self.previous_action = best_action

        return best_action

    def explore(self, u, n):
        """
        Chooses whether we should explore different actions, or stick to what we have done before
        [param] u utility function
        [param] n frequency (number of times) we did an state-action pair

        return some score
        """
        best_possible_reward = 10000
        frequency_max = 5

        print("explore:" + str(n) +" " + str(frequency_max))

        if n < frequency_max:
            return best_possible_reward
        else:
            return u
        
    # def returnState(wrld, x, y):
    #     """ Given a world, define the state for it"""


    #     # There are honestly too many states to consider if you treat each cell as an individual state along with the monsters..etc 
    #     # bomb
    #     #

    #     # position
    #     width = wrld.width
    #     height = wrld.height

    #     char_pos_state = height*y + x

    def reward_calc(self, previous_state, current_state):

        if current_state > previous_state: # we just got closer to the goal
            return 1.0
        else:
            return -1.0





