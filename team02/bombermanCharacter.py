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


class BombermanCharacter(CharacterEntity):

    WALK_PATH = 0
    AVOID_BOMB = 1
    WALK_BACK_TO_PATH = 2

    STATE = 0
    save_point = (0 , 0)

    possible_states = []
    possible_actions = []

    previous_state = None
    previous_action = None
    reward = None

    QTable = StateActionLookupTable(possible_states, possible_actions)
    NTable = NStateActionTable(possible_states, possible_actions)

    def do(self, wrld):
        pass

    def q_learning(self, current_state = None, reward = None):
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

            # Indicate that we tried the state-action
            self.NTable.update(s, a)

            # Update Q(s, a) using s', a' (current), s, a (past)
            n = self.NTable.get(s, a)
            max_q = get_max_q()
            q = self.QTable.get(s, a)

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

        if n < frequency_max:
            return best_possible_reward
        else:
            return u