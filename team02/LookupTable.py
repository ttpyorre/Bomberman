# Table for Action State Pairs
import sys
sys.path.insert(0, '../bomberman')

class StateActionLookupTable():

    states = []
    actions = []
    table = {}

    def __init__(self, states = [], actions = [] ):

        self.states = states
        self.actions = actions

        # create an empty dictionary that can be indexed by state and action
        for s in states:
            for a in actions:
                self.table[(s, a)] = 0.0

    def get(self, s , a):
        return self.table[(s,a)]

    def set(self, s, a, value):
        self.table[(s, a)] = value

    def update(self, s, a, value):
        self.table[(s,a)] += value

    def printit(self):

        print('S Table')
        # Print the names of the columns.
        print("{:<10} {:<20} {:<10}".format('STATE', 'ACTION', 'Q_VALUE'))
        
        # print each data item.
        for key, q_value in self.table.items():
            (state, action) = key
            if q_value != 0:
                print("{:<10} {:<20} {:<10}".format(state, str(action), q_value))
                



class NStateActionTable():
    """
    This table holds the frequency (number of times) we explored an state-action pair
    """

    states = []
    actions = []
    table = {}

    def __init__(self, states = [], actions = [] ):

        self.states = states
        self.actions = actions

        # create an empty dictionary that can be indexed by state and action
        for s in states:
            for a in actions:
                self.table[(s, a)] = 0

    def get(self, s , a):
        return self.table[(s,a)]

    def update(self, s, a):
        self.table[(s,a)] += 1

    def printit(self):
        
        # Print the names of the columns.
        print('N Table')
        print("{:<10} {:<10} {:<10}".format('STATE', 'ACTION', 'Q_VALUE'))
        
        # print each data item.
        for key, q_value in self.table.items():
            (state, action) = key
            print("{:<10} {:<10} {:<10}".format(state, action, q_value))
                
