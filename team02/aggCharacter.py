# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import search

class AggCharacter(CharacterEntity):

    def do(self, wrld):
        # Check(and get) monster location
        monster_co, is_monster_near = self.monster_nearby(wrld, 3)
        if is_monster_near != True:
            path = search.astar(self, wrld)
            print("move pepeag")
            walk = path.pop(0)
            self.move(walk[0] - self.x, walk[1] - self.y)
        else:
            
            self.move(0, 0)
            pass

    def monster_nearby(self, wrld, depth):
        '''
        BFS to check where the monster is, and if it is close.
        :param wrld         [SensedWorld]   Our world
        :param depth        [int]           Depth we search
        :return monst_co    [(int, int)]    Monster Location
        :return monst_e     [bool]          True if we saw a monster
        '''
        # We could also get World.monster values, but I prefer this
        start = (self.x, self.y)
        queue = [start]
        travelled = [start]
        at_depth = 0

        while queue:
            current = queue.pop(0)
            if wrld.monsters_at(current[0], current[1]):
               return current, True
            
            # Check neighbors
            neighbors = search.neighbors_of_8(wrld, current[0], current[1])
            for neighbor in neighbors:
                if neighbor not in travelled:
                    queue.append(neighbor)
                    travelled.append(neighbor)


            if at_depth == 0 and depth != 0:
                at_depth = len(queue)
                depth -= 1
            elif depth == 0:
                # we are done searching, no need to search futher
                break
            else:
                at_depth -= 1
        return [], False


    def minimax(self, wrld, depth):
        '''
        :param depth
        :param alpha
        :param beta
        :return location we should move to
        '''
        path = []
        depth = depth*2 
        curr_depth = 0

        newwrdl = SensedWorld.from_world(wrld)

        AggCharacter.min_val(newwrld, depth, curr_depth)


        print(path)
        return path

    @staticmethod
    def max_val(wrld, depth, curr_depth):
        '''
        '''
        curr_depth += 1
        # First check for terminal state
        if self.terminal_state(wrld):
            return self.terminal_utility(wrld)
        
        
        # We check the bombermans moves at this stage
        for dx in [-1, 0, 1]:
            if .x + dx >= 0 and monst.x + dx < wrld.width():
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0 and monst.y + dy >= 0 and monst.y + dy < wrld.height():
                        if not wrld.wall_at(monst.x + dx, monst.y + dy):
                            monst.move(dx, dy)
                            (newwrld, events) = wrld.next()
        
    @staticmethod
    def min_val(wrld, depth, curr_depth):
        '''
        '''
        curr_depth += 1
        # First check for terminal state
        if self.terminal_state(wrld):
            return self.terminal_utility(wrld)
        
        monst = next(iter(wrld.monsters.values()))
        
        # We check the monsters moves at this stage
        for dx in [-1, 0, 1]:
            if monst.x + dx >= 0 and monst.x + dx < wrld.width():
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0 and monst.y + dy >= 0 and monst.y + dy < wrld.height():
                        if not wrld.wall_at(monst.x + dx, monst.y + dy):
                            monst.move(dx, dy)
                            (newwrld, events) = wrld.next()




    @staticmethod
    def reward(wrld, curr_co, monst_co):
        '''
        '''
        R = 0 # set R
        
        # distance to goal
        goal = wrld.exit_cell
        goal_weight = 3
        R += goal_weight*(1 / search.euclidean(curr_co, goal))
        
        # distance to monster
        dist_to_monst = search.euclidean(curr_co, monst_co)
        if dist_to_monst < 2:
            R -= 3
        elif dist_to_monst < 3:
            R -= 2
        elif dist_to_monst < 4:
            R -= 1

        return R

    def terminal_state(self, wrld):
        '''
        '''
        # look at ALL monsters
        if wrld.monsters_at(self.x, self.y):
            return True


        if wrld.exit_at(self.x, self.y):
            return True

        return False

    def terminal_utility(self, wrld):
        '''
        '''
        # look at ALL monsters
        if wrld.monsters_at(self.x, self.y):
            return -10000


        if wrld.exit_at(self.x, self.y):
            return 10000

        return 0
        


