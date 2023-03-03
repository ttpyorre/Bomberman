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


def get_char_available_actions(wrld, x, y):
    """
    Gets the available moves at position x, y, and use of bombs
        Checks if the neighboring cells are empty (excluding the character or the exit)
        Checks if the neighbor is within range of the bomb's explosion
    """ 

    def empty_at(x_, y_):        
        # return (not wrld.wall_at(x_,y_) and wrld.bomb_at(x_,y_) == None and wrld.explosion_at(x_,y_) == None and wrld.monsters_at(x_,y_) == None )
        # return wrld.bomb_at(x_, y_) == None
        if wrld.exit_at(x_, y_): return True
        elif wrld.empty_at(x_, y_): return True

        return False

    def filter_for_safe_cells(neighbors = []):
        l = []

        for n in neighbors:
            if empty_at(n[0], n[1]):
                print("Step 1")
                if not search.in_range_of_bomb(wrld, x, y):
                    print("Step 2")
                    l.append(n)
        
        return l

    n_of_8 = filter_for_safe_cells(search.neighbors_of_8(wrld, x, y))
    n_of_4_corners = filter_for_safe_cells(search.neighbors_of_4_corners(wrld, x, y))

    # n_of_8 = search.neighbors_of_8(wrld, x, y)
    # n_of_4_corners = search.neighbors_of_4_corners(wrld, x, y)

    print("n of 8: " + str(n_of_8))
    print("n of 4: " + str(n_of_4_corners))

    actions = []

    # All the actions that are safe without cosidering using the bomb
    for n in n_of_8:
        actions.append((n[0] - x, n[1] - y, False))
    # the rest of the actions involving the bomb. We are exculding moves 
    #   that will put the character in range of the bomb
    for n in n_of_4_corners:
        actions.append((n[0] - x, n[1] - y, True))

    bomb_exist = False
    return actions

def get_all_possible_actions():
    """
    Gets all possible actions the char can do. Doesnt IGNORE any actions.
        Doesnt care about:
            Out of bounds
            Walls
            Monsters
            Bombs
            Explosions
    """
    actions = []

    # movements without using bombs
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            actions.append((dx, dy, False))

    # movements with bombs
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            actions.append((dx, dy, True))

    return actions

def get_all_states(wrld_width, wrld_height, wall_loc = []):
    """
    Gets a list of the wrld state represenation
    """

    # cells = wrld_wdith * wrld_height
    max_walls = len(wall_loc)
    

    states = []

    for x in range(wrld_width):
        for y in range(wrld_height):
            for w in range(max_walls + 1):
                for active_bomb in [0, 1]:
                    states.append((x, y, w, active_bomb))

    return states

def get_num_of_broken_walls(wrld, wall_loc = []):
    """
    treating an unbroken wall as all the cells of a row to be walls
    """
    broken_walls = 0

    for row in wall_loc:
        for col in range(wrld.width()):
            if wrld.wall_at(col, row): pass
            else:
                broken_walls += 1
                break

    return broken_walls



# def get_all_possible_actions():
#     actions = []

#     for dx in [-1, 0, 1]:
#         for dy in [-1, 0, 1]:
#             actions.append((dx, dy, False))
#     return actions


# def get_char_available_actions(wrld, x, y):
#     """
#     Gets the available moves at position x, y, and us of bombs
#         Note, only checks for walls, or out of bounds
#     """ 

#     # check to see if a bomb exist

#     bomb_exist = False

#     try:
#         bomb = next(iter(wrld.bombs.values()))[0]
#         bomb_exist = True
#     except:
#         print("no bombs exist")
    
#     actions = []

#     for dx in [-1, 0, 1]:
#         if x + dx >= 0 and x + dx < wrld.width():
#             for dy in [-1, 0, 1]:
#                 if (dx != 0 or dy != 0) and y + dy >= 0 and y + dy < wrld.height():
#                     if not wrld.wall_at(x + dx, y + dy):

#                         # add as a possible action to place a bomb and move
#                         # regardless of the situation, we should be allowed to move without placing a bomb
#                         actions.append((dx, dy, False))

#     return actions





class BombermanCharacter(CharacterEntity):

    
    save_point = (0 , 0)

    all_states = get_all_states(8, 5, [3])  
    # states are defined as (x, y, bomb_active, num_broken_walls) 
    # where:
    #   char x location
    #   char y location
    #   bomb active is [0 or 1] for not active, and active
    #   num_broken_walls is the number of broken walls in the world


    all_actions = get_all_possible_actions()

    possible_actions = []
    
    previous_state = (0, 0, 0, 0)  # <- init state
    previous_action = (0,0,False)  # Do nothing
    

    QTable = StateActionLookupTable(all_states, all_actions)
    NTable = NStateActionTable(all_states, all_actions)

    def do(self, wrld):

        # print(self.all_actions)
        # print(get_char_available_actions(wrld, self.x, self.y))
        # a state is represented as (cell_location, bomb_active, num_broken_walls)

        # Get the current state, actions, and the reward as the result of being in this state
        current_state = self.get_wrld_state(wrld)
        self.possible_actions = get_char_available_actions(wrld, self.x, self.y)
        reward = self.reward_calc(wrld, self.previous_state, current_state)


        # print("prev:" + str(self.previous_state) + "curr:" + str(current_state))

        # print(str(current_state), str(reward))
        action = self.q_learning(current_state, reward)
        # self.QTable.printit()

        # print(str(action))
        self.execute_action(action[0], action[1], action[2])

        

    def get_wrld_state(self, wrld):

        # (x, y,  bomb_active, # of broken walls)
        bomb_active = search.is_bomb_active(wrld)
        num_broken_walls = get_num_of_broken_walls(wrld)
        return (self.x, self.y, bomb_active, num_broken_walls)

    def execute_action(self, dx, dy, use_bomb):
        self.move(dx, dy)
        if use_bomb: self.place_bomb()

    def get_max_q(self, current_state):
        max_q = float("-inf")
        for a in self.possible_actions:
            q = self.QTable.get(current_state, a)
            

            if max_q == None or q > max_q:   
                max_q = q

        return max_q

    def q_learning(self, current_state = None, reward = 0):
        """
        current_state   - (s') the current state of the character
        reward          - R(s, a, s') the reward we just got from doing an action
        """

        s = self.previous_state
        a = self.previous_action

        learning_rate = 0.2 
        discount = 0.9
        
        if s != None:

            # # Indicate that we tried the state-action
            self.NTable.update(s, a)

            # Update Q(s, a) using s', a' (current), s, a (past)
            n = self.NTable.get(s, a)
            max_q = self.get_max_q(current_state)
            q = self.QTable.get(s, a)

            print("Reward: " + str(reward))
            print(discount*max_q - q)

            value = learning_rate*(reward + discount*max_q - q)
            self.QTable.update(s, a, value)

        # choose the best action (unexplored action or best util)
        best_action = self.get_best_action(current_state)

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
        best_possible_reward = 10
        frequency_max = 2

        # print("explore:" + str(n) +" " + str(frequency_max))

        if n < frequency_max:
            return best_possible_reward
        else:
            return u
        
    def get_best_action(self, current_state):
        """
        Based on the current state return the best action
        """
        max_value = None
        best_a = None
        for a in self.possible_actions:

            # value = self.explore(self.QTable.get(current_state, a), self.NTable.get(current_state, a))
            value = self.QTable.get(current_state, a)
            
            if max_value == None or value > max_value:   
                max_value = value
                best_a = a

        return best_a
    
    # def returnState(wrld, x, y):
    #     """ Given a world, define the state for it"""


    #     # There are honestly too many states to consider if you treat each cell as an individual state along with the monsters..etc 
    #     # bomb
    #     #

    #     # position
    #     width = wrld.width
    #     height = wrld.height

    #     char_pos_state = height*y + x

    def reward_calc(self, wrld, previous_state, current_state):

        # (cell_location, bomb_active, num_broken_walls)
        

        reward = 0.0

        # cell_location
        prev_dis = search.euclidean((previous_state[0], previous_state[1]), wrld.exitcell)
        curr_dis = search.euclidean((current_state[0], current_state[1]), wrld.exitcell)
        reward += prev_dis - curr_dis

        # bomb_active
        if current_state[2]:
            # if we are in range of the bomb, then -
            if search.in_range_of_bomb(wrld, current_state[0], current_state[1]): reward += -10.0

            # if it opens up a wall +
            if search.wall_in_range_of_bomb(wrld): reward += 5.0
            

        # num_broken_walls
        
        reward += (current_state[3] - previous_state[3])*10


        return reward
        

        # if current_state > previous_state: # we just got closer to the goal
        #     return 1.0
        # else:
        #     return -1.0





