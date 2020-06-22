"""
2020.06.16
Authors: N. Seelam (nseelam1@gmail.com), D.K. Murakowski (murakdar@gmail.com)

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
XX 5. move_direc (left/right/up/down)
    For a cardinal direction, move all tiles in that direction as far as they can go
XX 6. merge_tiles
    Tiles that are adjacent to one another will merge to create an N + N tile

"""
import numpy as np
from collections import Counter
from itertools import groupby

class game2048():
    """
    Create an initialized version of 2048
    """

    def __init__(self, 
                 GRID_LENGTH, 
                 MAX_POWER, 
                 MAX_GEN):
        """
        Initialize gameboard.

        GRID_LEN   - size of square dimensional gameboard
        MAX_POWER  - maximum tile possible to generate before end game
        MAX_GEN    - max size tile to generate [multiple of 2]
        KEYSTROKES - key strokes for the cardinal directions (and alt. bindings)

        Game continues until self.game_outcome != None
        """
        self.GRID_LENGTH = GRID_LENGTH
        self.MAX_POWER = MAX_POWER
        self.MAX_GEN = MAX_GEN
        self.board = None
        self.make_gameboard(GRID_LENGTH)
        self.board[np.random.randint(GRID_LENGTH), np.random.randint(GRID_LENGTH)] = 2

    def make_gameboard(self, N=None):
        """
        Create an N x N grid for 2048.
        Standard game is a 4 x 4.
        """
        if self.board is not None:
            print('Erasing board for new game.')

        if N is None:
            N = self.GRID_LENGTH

        self.board = np.zeros(shape=(N, N)).astype(int)
        self.game_outcome = None
        self.score = 0

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
            self.board[pos] = keys[np.where(np.random.random() <= prior)[0][0]]

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

    @staticmethod
    def shift(row):
        """
        Pushes all non-zero values to the leftmost.
        """
        nnz = row[row!=0]
        pad = np.zeros(len(row) - len(nnz))
        return np.concatenate((nnz, pad))

    @staticmethod
    def merge(row):
        """
        Shift and merge tiles.
        Defaults to left. The move_direc will handle
        all cardinal directions
        """
        def result(value, elements):
            quotient, remainder = divmod(len(list(elements)), 2)
            return [2*value]*quotient + [value]*remainder
        nnz = np.concatenate([result(k, g) for k, g in groupby(row)])
        pad = np.zeros(len(row) - len(nnz))
        return np.concatenate((nnz, pad))

    @staticmethod
    def move_all_left(row_i): return np.apply_along_axis(move_row_left, 1, row_i)

    @staticmethod
    def move_all_up(row_i): return np.apply_along_axis(move_row_left, 0, row_i)

    @staticmethod
    def move_row_left(row): return game2048.merge(game2048.shift(row))


moveset = {
    'left': game2048.move_all_left,
    'right': lambda b: np.fliplr(move_all_left(np.fliplr(b))),
    'up': game2048.move_all_up,
    'down': lambda b: np.flipud(move_all_up(np.flipud(b))),
}

    #@staticmethod
    #def move_direc(board, direction):
    #    """Shift and merge all tiles of board in the given cardinal direction
    #
    #    Inputs:
    #    board - a 2-dimensional array
    #    direction - 'left', 'right', 'up', or 'down'
    #    """
    #    # The most basic operation is to shift and merge a single row left.
    #    # Such an operation can then be applied to all rows or all columns,
    #    # transposing / rotating / reflecting the board as needed, to cover
    #    # all four directions (left / right / up / down).
    #    def move_row_left(row):
    #        def shift(row):  # squeeze non-zero elements together
    #            nnz = row[row!=0]
    #            pad = np.zeros(len(row) - len(nnz))
    #            return np.concatenate((nnz, pad))
    #        def merge(row):
    #            def result(value, elements):
    #                quotient, remainder = divmod(len(list(elements)), 2)
    #                # TODO: preserve array dtype? this currently returns list
    #                return [2*value]*quotient + [value]*remainder
    #            nnz = np.concatenate([result(k, g) for k, g in groupby(row)])
    #            pad = np.zeros(len(row) - len(nnz))
    #            return np.concatenate((nnz, pad))
    #        return merge(shift(row))
    #
    #    def move_all_left(b): return np.apply_along_axis(move_row_left, 1, b)
    #    def move_all_up(b): return np.apply_along_axis(move_row_left, 0, b)
    #    func = {
    #        'left': move_all_left,
    #        'right': lambda b: np.fliplr(move_all_left(np.fliplr(b))),
    #        'up': move_all_up,
    #        'down': lambda b: np.flipud(move_all_up(np.flipud(b))),
    #    }
    #
    #    return func[direction](board)

