"""
2020.06.16

The following is the code-base for a pythonic 2048 game.

The script has the following functions:

XX 1. make_board 
    initialize a new game-board; should be 4 x 4 but can be n x n
XX 2. find_pos
    Find all valid tiles in the game that can be used to generate
    a new piece
XX 3. choose_pos
    If there are valid tiles, choose a tile
XX 4. generate_tile
    For a chosen position, choose a value for the tile.
    Ideally, this is dynamic based on the largest tile available
5. move_direc (left/right/up/down)
    For a cardinal direction, move all tiles in that direction as far as they can go
6. merge_tiles
    Tiles that are adjacent to one another will merge to create an N + N tile

"""
import numpy as np
from collections import Counter

class game2048():
    """
    Create an initialized version of 2048
    """

    def __init__(self, 
                 GRID_LEN=4, 
                 MAX_POWER=17,
                 MAX_GEN=2):
        """
        Initialize gameboard.

        N - size of square dimensional gameboard
        max_power - maximum tile possible to generate before end game
        max_gen   - max size tile to generate [multiple of 2]

        Game continues until self.game_outcome != None
        """
        self.GRID_LEN = GRID_LEN
        self.make_gameboard(GRID_LEN)

    def make_gameboard(self):
        """
        Create an N x N grid for 2048.
        Standard game is a 4 x 4.
        """
        self.board = np.zeros(shape=(self.GRID_LEN, self.GRID_LEN))
        self.game_outcome = None

    def choose_pos(self):
        """
        Given all valid areas on the board,
        randomly generate a square (equally likely anywhere)
        with a specific value.

        If there are no available positions to generate,
        evaluate as 'lost'. 
        """
        idx = self.find_pos(self.board)
        if len(idx):
            pos = idx[np.random.randint(low=0, high=len(idx))]
            keys, prior = self.generate_tile(self.board, self.MAX_GEN)
            board[pos] = keys[np.where(np.random.random() <= prior)[0][0]]

        else:
            self.game_outcome = 'LOSE' 

    """ The following methods are atomistic rules toward finding positions,
    generating tiles, and merging"""

    @staticmethod
    def find_pos(board):
        """
        Find all tiles that are capable of having
        a newly generated tile in.
        """
        i, j = np.where(board == 0)
        return list(zip(i,j))

    @staticmethod
    def generate_tile(board, MAX_GEN, ENSURE_24=True, p=2):
        """
        Generate a tile that is a multiple of 2.
        This is on a sliding scale, where you can
        only generate tiles that are at most, the
        highest order N of the number currently available.

        Inputs:
        board - the gameboard with current scores
        max_power -maximum sized tile to generate
        ENSURE_24 - Assure 2s and 4s are in the distribution
        p - fraction of 2s/4s in the distribution

        """
        # Generate a prior
        counts = Counter(list(np.ndarray.flatten(board[(board > 0) & (board <= 2**MAX_GEN)])))

        if sum(counts.values()) == 0:
            counts[2] = 1
            counts[4] = 1
        else:
            Nsum = sum(counts.values())
            if ENSURE_24 is True:  
                counts[2] = round(Nsum/p)
                counts[4] = round(Nsum/p)
                #if counts[2] == 0:
                #    counts[2] = round(Nsum/p)
                #if counts[4] == 0:
                #    counts[4] = round(Nsum/p)

        prior = [counts[key] for key in sorted(counts.keys()) if key <= 2**MAX_GEN]
        prior = np.cumsum(prior)/sum(counts.values())

        return list(sorted(counts.keys())), prior


