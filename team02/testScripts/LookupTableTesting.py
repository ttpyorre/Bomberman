#!/usr/bin/enb python3

# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff

from LookupTable import StateActionLookupTable, NStateActionTable


actions = [1, 2, 3, 4]
states = [1, 2, 3, 4, 5, 6]

STable = StateActionLookupTable(states, actions)
NTable = NStateActionTable(states, actions)
STable.printit()


print("Stable Length:" + str(len(STable.table)))


STable.set(1, 1, 1.5)
print(STable.get(1, 1))
STable.update(1, 1, 1.0)
print(STable.get(1, 1))
STable.update(1, 1, -2.0)
print(STable.get(1, 1))
STable.printit()

NTable.update(1, 1)
NTable.update(1, 1)
NTable.update(1, 2)

NTable.printit()


