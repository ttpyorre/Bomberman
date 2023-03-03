# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

from events import Event
from game import Game

# Import necessary stuff

from bombermanCharacter2 import BombermanCharacter2


class TestBombermanCharacter2(BombermanCharacter2):

    def do(self, wrld):
        
        # self.testReward()
        # self.testGetChar(wrld)
        # self.testFeatures(wrld)
        pass
        

    @staticmethod
    def testReward():
        print("Testing reward")

        player1 = BombermanCharacter2("mini", "c", 0, 2)

        eWall = Event(0, player1)
        eBombMon = Event(1, player1)
        eBombChar = Event(2, player1)
        eMon = Event(3, player1)
        eExit = Event(4, player1)

        # BOMB_HIT_WALL               = 0
        # BOMB_HIT_MONSTER            = 1
        # BOMB_HIT_CHARACTER          = 2
        # CHARACTER_KILLED_BY_MONSTER = 3
        # CHARACTER_FOUND_EXIT        = 4

        events_mon = [eMon, eBombChar, eExit]
        events_bomb = [eBombChar, eExit]
        events_exit = [eExit]
        events_any = []
        print(player1.reward(events_mon))
        print(player1.reward(events_bomb))
        print(player1.reward(events_exit))
        print(player1.reward(events_any))

    
    def testGetChar(self, wrld):
        print("Testing get char")

        char_exist = self.get_char(wrld)
        char_none = self.get_char(None)

        print(char_exist.x == self.x)
        print(None == char_none)

    def testFeatures(self, wrld):
        if wrld.exitcell[0] == 7:
            print("Our assuption is correct")
            
            f1_list = self.features(3, 0, wrld)
            fl_expectation = [1.0/5.0, 1.0, 1.0]
            print(f1_list == fl_expectation)

            f1_list = self.features(2, 0, wrld)
            fl_expectation = [1.0/6.0, 1.0, 1.0]
            print(f1_list == fl_expectation)

            f1_list = self.features(1, 0, wrld)
            fl_expectation = [1.0/7.0, 1.0, 1.0]
            print(f1_list == fl_expectation)


#++++++++++++++++++++++++++++++++++ Creating the Game +++++++++++++++++++

g = Game.fromfile('flatline_map.txt')

g.add_character(TestBombermanCharacter2("mini", # name
                              "C",  # avatar
                              3, 0  # position
))

# Run!
g.go()

    





