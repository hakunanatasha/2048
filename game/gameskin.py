"""
2020.06.18

N.Seelam Gameboard construction of 2048

These are the sets of constants

"""
from rules import moveset
# GAME PARAMETERS
GRID_LENGTH = 4
MAX_POWER = 15 # Max sized tile before game won
MAX_GEN = 2    # 

# GAME AESTHETICS

# Parameters for the gameboard
BOARD_X = 600
BOARD_Y = 620
BOARD_SIZE = str(BOARD_X) + "x" + str(BOARD_Y)

SIZE_X = 500
SIZE_Y = 500 
GRID_PADDING = 5

GAME_FONT = "Calibri"
GAME_TITLE_SIZE = 50
GAME_FONT_SIZE = 40
TITLE_COLOR = '#393939'

BACKGROUND_COLOR_GAME = "#E4E4E4"

# Cell Parameters
#CELL_LABEL_TEXT_WIDTH  = 5
#CELL_LABEL_TEXT_HEIGHT = 2

TEXT_DICT = {int(2**idx): str(int(2**idx)) for idx in range(1,MAX_POWER)}
TEXT_DICT.update({0: ""})
BACKGROUND_COLOR_DICT = {0: "#959494",
                         2: "#eee4da", 
                         4: "#ede0c8", 
                         8: "#f2b179",
                         16: "#f59563", 
                         32: "#f67c5f", 
                         64: "#f65e3b",
                         128: "#edcf72", 
                         256: "#edcc61", 
                         512: "#edc850",
                         1024: "#edc53f", 
                         2048: "#edc22e",
                         4096: "#eee4da", 
                         8192: "#edc22e", 
                         16384: "#f2b179",
                         32768: "#f59563", 
                         65536: "#f67c5f"}

TEXT_COLOR_DICT = {0: "#776e65", # This was the original color of 2/4
                   2: "#696563", 
                   4: "#696563", 
                   8: "#f9f6f2", 
                   16: "#f9f6f2",
                   32: "#f9f6f2", 
                   64: "#f9f6f2", 
                   128: "#f9f6f2",
                   256: "#f9f6f2", 
                   512: "#f9f6f2", 
                   1024: "#f9f6f2",
                   2048: "#f9f6f2",
                   4096: "#776e65", 
                   8192: "#f9f6f2", 
                   16384: "#776e65",
                   32768: "#776e65", 
                   65536: "#f9f6f2"}

FONT = ("Verdana", 40, "bold")

# Keyboard commands

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

# Key-stroke commands
KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"
KEY_BACK = "'b'"

KEY_J = "'j'"
KEY_K = "'k'"
KEY_L = "'l'"
KEY_H = "'h'"

commands = {
    KEY_UP: moveset['up'], 
    KEY_DOWN: moveset['down'],
    KEY_LEFT: moveset['left'], 
    KEY_RIGHT: moveset['right'],
    KEY_UP_ALT: moveset['up'],
    KEY_DOWN_ALT: moveset['down'],
    KEY_LEFT_ALT: moveset['left'],
    KEY_RIGHT_ALT: moveset['right'],
    KEY_H: moveset['left'],
    KEY_L: moveset['right'],
    KEY_K: moveset['up'],
    KEY_J: moveset['down'],
}

x_axis_labels = ('x1', 'x2', 'x3', 'x4')
y_axis_labels = ('y1', 'y2', 'y3', 'y4')

