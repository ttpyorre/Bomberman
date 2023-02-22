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


class BombermanCharacter(CharacterEntity):

    WALK_PATH = 0
    AVOID_BOMB = 1
    WALK_BACK_TO_PATH = 2

    STATE = 0
    save_point = (0 , 0)

    def do(self, wrld):

        print(self.STATE)

        if self.STATE == self.WALK_PATH:

            # Get a path ignoring the walls
            path = search.astar(self, wrld, wrld.exitcell, True)
            for p in path: self.set_cell_color(p[0], p[1], Fore.RED + Back.BLUE)

            while path:
                walk = path.pop()

                if wrld.wall_at(walk[0], walk[1]):
                    # Save the desired position to get back to the spot later
                    self.save_point = walk

                    # Place the bomb to open the wall
                    print("wall stopping us")
                    self.place_bomb()
                    self.STATE = self.AVOID_BOMB
                    
                    # we also need to get out of the range of the bomb
                    corner = search.neighbors_of_4_corners(wrld, self.x, self.y)

                    # choose any available corner to go to
                    c = corner.pop()
                    self.set_cell_color(c[0], c[1], Fore.RED + Back.YELLOW)
                    self.move(c[0] - self.x, c[0] - self.y)

                else:
                    self.move(walk[0] - self.x, walk[1] - self.y)


        elif self.STATE == self.AVOID_BOMB:
            # we already moved out of the way, so do nothing
            self.move(0,0)
            if not search.is_bomb_active(wrld) and not search.explosions_exist(wrld):
                print("swtich states")
                self.STATE = self.WALK_BACK_TO_PATH

        elif self.STATE == self.WALK_BACK_TO_PATH:
            print(self.save_point)
            
            # find a new save point
            if wrld.wall_at(self.save_point[0], self.save_point[1]):
                alt = search.neighbors_of_8(wrld, self.save_point[0], self.save_point[1])
                dis = search.euclidean(self.save_point, wrld.exitcell)

                for a in alt:
                    d = search.euclidean(a, wrld.exitcell)
                    if d < dis: self.save_point = a

            # if (self.x, self.y) == self.save_point:
            #     self.STATE = self.WALK_PATH
            # else:
            # Get a path ignoring the walls
            path = search.astar(self, wrld, self.save_point)
            for p in path: self.set_cell_color(p[0], p[1], Fore.RED + Back.YELLOW)

            if len(path) == 0:
                self.STATE = self.WALK_PATH
            else:
                print(path)

                while path:
                    walk = path.pop()
                    self.move(walk[0] - self.x, walk[1] - self.y)

    def astar(self, wrld, goal, ignore_walls = False):
        return search.astar(self, wrld, goal, ignore_walls)