# Table for Action State Pairs
import sys
sys.path.insert(0, '../bomberman')

class StateActionLookupTable():

    table = {}

    def __init__(self, states = [], actions = [] ):

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

class NStateActionTable(StateActionLookupTable):
    """
    This table holds the frequency (number of times) we explored an state-action pair
    """

    def update(self, s, a):
        """
        Add 1 to the state-action we just did, and update the table accordingly
        """
        self.table[(s, a)] += 1.0
