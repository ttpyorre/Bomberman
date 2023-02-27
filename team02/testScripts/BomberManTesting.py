# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff

from bombermanCharacter import BombermanCharacter

player1 = BombermanCharacter("mini", "c", 0, 2)

# reward function
print(player1.reward_calc(previous_state = 0, current_state = 1) == 1.0)
print(player1.reward_calc(previous_state = 1, current_state = 0) == -1.0)

# explore function
print(player1.explore(-100.0, 1) == 10000)
print(player1.explore(-100.0, 5) == -100.0)
print(player1.explore(-100.0, 6) == -100.0)


player2 = BombermanCharacter("mini", "c", 0, 3)
player2.possible_actions = [(0,0, False), (0, 1, False), (1, 1, False)]

player2.QTable.set(2,(0, 0, False), value = 6.0)
player2.QTable.set(2,(0, 1, False), value = 5.0)
player2.QTable.set(2,(1, 1, False), value = -1.0)
print(player2.get_max_q(2) == 6.0)

print(player2.get_best_action(2) == (0, 0, False))


