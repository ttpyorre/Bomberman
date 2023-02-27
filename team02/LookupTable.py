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

        print(self.table)
                



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
        print(self.table)
                
