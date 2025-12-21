import os
import sys
sys.path.insert(0, os.getcwd())
from test_run import test_and_run

dirname = os.path.dirname(__file__)
testfile = os.path.join(dirname, "test.txt")
inputfile = os.path.join(dirname, "input.txt")

class Rock:
    WIDHT = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prev_x = x
        self.falling = True

    def push_right(self):
        if self.x + self.WIDTH - 1 < 6:
            self.prev_x = self.x
            self.x += 1


    def push_left(self):
        if self.x > 0:
            self.prev_x = self.x
            self.x -=1

    def fall(self):
        self.y -=1
    
    def undo_last_move(self):
        self.x = self.prev_x
    
    def undo_fall(self):
        self.y += 1
    
    @property
    def tiles(self):
        return {(self.x + x, self.y + y) for x,y in self.TILES}
    
    def collides(self, other_rocks):
        if self.y >= len(other_rocks):
            return False
        for x,y in self.tiles:
            if y >= len(other_rocks):
                continue
            if x in other_rocks[y]:
                return True
        return False
    
    @property
    def top(self):
        return self.y + self.HEIGHT


class HorizontalLineRock(Rock):
    WIDTH = 4
    HEIGHT = 1
    TILES =  [(0,0), (1,0), (2,0), (3,0)]
    """
    ####
    """

class VerticalLineRock(Rock):
    WIDTH = 1
    HEIGHT = 4
    TILES = [(0,0), (0,1), (0,2), (0,3)]
    """
    #
    #
    #
    #
    """
class PlusRock(Rock):
    WIDTH = 3
    HEIGHT = 3
    TILES = [(0,1), (1,2), (1,1), (1,0), (2,1)]
    """
    .#.
    ###
    .#.
    """

class LRock(Rock):
    WIDTH = 3
    HEIGHT = 3
    TILES =  [(0,0), (1,0), (2,0), (2,1), (2,2)]
    """
    ..#
    ..#
    ###
    """

class SquareRock(Rock):
    WIDTH = 2
    HEIGHT = 2
    TILES = [(0,0), (1,0), (0,1), (1,1)]
    """
    ##
    ##
    """

ROCK_ORDER = [HorizontalLineRock, PlusRock, LRock, VerticalLineRock, SquareRock]

def main(filename):
    with open(filename) as f:
        lines = f.readlines()

    move_sequence = lines[0].strip()

    rocks = []
    y_max = -1
    move_counter = 0
    for rock_counter in range(2023):
        RockType = ROCK_ORDER[rock_counter % len(ROCK_ORDER)]
        rock = RockType(2, y_max + 4)
        while rock.falling:
            move = move_sequence[move_counter % len(move_sequence)]
            if move == "<":
                rock.push_left()
            else:
                rock.push_right()
            move_counter += 1

            if rock.collides(rocks):
                rock.undo_last_move()
            
            
            rock.fall()
            if rock.y < 0:
                rock.undo_fall()
                rock.falling = False
            else:
                if rock.collides(rocks):
                    rock.undo_fall()
                    rock.falling = False
       
        while len(rocks) < rock.top:
            rocks.append([])
        for x,y in rock.tiles:
            rocks[y].append(x)

        y_max = max(y_max, len(rocks)-1)

    return y_max -1


EXPECTED_TEST_RESULT = 3068
test_and_run(main, testfile, EXPECTED_TEST_RESULT, inputfile)
