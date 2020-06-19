import unittest
from game.rules import game2048


class GameTestCase(unittest.TestCase):
    def test_movement_nongreedy(self):
        board = [[2, 2, 2, 2, 2, 0]]
        self.assertSequenceEqual(game2048.move_direc(board, 'left').tolist(),
                                 [[4, 4, 2, 0, 0, 0]])  # not [[8,2,0,0,0,0]]
        self.assertSequenceEqual(game2048.move_direc(board, 'right').tolist(),
                                 [[0, 0, 0, 2, 4, 4]])  # not [[0,0,0,0,2,8]]

    def test_movement_move_direction_priority(self):
        board = [[2], [2], [2], [8]]
        self.assertSequenceEqual(game2048.move_direc(board, 'up').tolist(),
                                 [[4], [2], [8], [0]])  # not [[2],[4],[8],[0]]
        self.assertSequenceEqual(game2048.move_direc(board, 'down').tolist(),
                                 [[0], [2], [4], [8]])  # not [[0],[4],[2],[8]]


if __name__ == '__main__':
    unittest.main()
