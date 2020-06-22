#!/usr/bin/env python3
"""
2020.06.21
Todo: Make sure you cannot get a dead move

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
                 GRID_LENGTH=4, 
                 MAX_POWER=17, 
                 MAX_GEN=2):
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

        # Moves
        self.moveset = {'left': self.move_all_left,
                        'right': lambda b: np.fliplr(self.move_all_left(np.fliplr(b))),
                        'up': self.move_all_up,
                        'down': lambda b: np.flipud(self.move_all_up(np.flipud(b)))}

    def make_gameboard(self, N=None):
        """
        Create an N x N grid for 2048.
        Standard game is a 4 x 4.
        """
        if self.board is not None:
            print('Erasing board for new game.')

        if N is None:
            N = self.GRID_LENGTH

        self.board = np.zeros(shape=(N, N))
        self.game_over = False
        self.score = 0
        self.move_score = 0

    def choose_pos(self):
        """
        Given all valid areas on the board,
        randomly generate a square (equally likely anywhere)
        with a specific value.

        If there are no available positions to generate,
        evaluate as 'lost'. 
        """
        # Find all available positions
        idx = self.find_pos(self.board)

        # If there are free spots, generate tile else quit
        if len(idx):
            pos = idx[np.random.randint(low=0, high=len(idx))]
            keys, prior = self.generate_tile_2or4(self.board)
            #keys, prior = self.generate_tile(self.board, self.MAX_GEN)
            self.board[pos] = keys[np.where(np.random.random() <= prior)[0][0]]

        else:
            self.game_over = True

    def move_tiles(self, direction):
        """
        Given a direction (up/down/left/right)
        evaluate the board.
        """
        new_board = self.moveset[direction](self.board)

        # Omit a dead move
        if (new_board != self.board).sum() > 0:
            self.score += self.move_score
            self.move_score = 0
            self.board = new_board
            self.choose_pos()

    def merge(self, row):
        """
        Shift and merge tiles.
        Defaults to left. The move_direc will handle
        all cardinal directions
        """
        output = list(zip(*[game2048.result(k, g) for k, g in groupby(row)]))
        nnz = np.concatenate(output[0])
        pad = np.zeros(len(row) - len(nnz))
        scoreval = sum(output[1])
        self.move_score += scoreval
        return np.concatenate((nnz, pad))

    # Moves Possible
    def move_all_left(self, row_i): return np.apply_along_axis(self.move_row_left, 1, row_i)

    def move_all_up(self, row_i): return np.apply_along_axis(self.move_row_left, 0, row_i)

    def move_row_left(self, row): return self.merge(game2048.shift(row))

    """ 
    The following methods are atomistic rules toward finding positions,
    generating tiles, and merging
    """

    # Required for generating new tiles
    @staticmethod
    def find_pos(board):
        """
        Find all tiles that are capable of having
        a newly generated tile in.
        """
        i, j = np.where(board == 0)
        return list(zip(i,j))

    @staticmethod
    def generate_tile_2or4(board):
        """ Generate a prior on 2s and 4s"""
        return [2, 4], np.array([0.8, 1])

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
            counts[4] = 0.25
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

    # Required for Movement
    @staticmethod
    def result(value, elements):
        quotient, remainder = divmod(len(list(elements)), 2)
        return [2*value]*quotient + [value]*remainder, 2*value*quotient

    @staticmethod
    def shift(row):
        """
        Pushes all non-zero values to the leftmost.
        """
        nnz = row[row!=0]
        pad = np.zeros(len(row) - len(nnz))
        return np.concatenate((nnz, pad))


