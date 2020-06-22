"""
2020.06.21

Tkinter playable 2048.

"""
import numpy as np
import sys

from tkinter import *
from tkinter import messagebox

# Game Mechanics/Aesthetics
from game.gameskin import *
from game.rules import game2048, moveset

# -------------- #
# Call the mechanics of the game
GameBoard = game2048(GRID_LENGTH=GRID_LENGTH, 
                     MAX_POWER=MAX_POWER,
                     MAX_GEN=MAX_GEN)

# -------------- #
# Set up the game sizes
master = Tk()
master.title("2048")
master.geometry(BOARD_SIZE)
master.configure(bg=BACKGROUND_COLOR_GAME)

# Set up game title
game_title = Label(master, text="2048", fg=TITLE_COLOR)
game_title.config(font=(GAME_FONT, GAME_FONT_SIZE, "bold"),
                  bg=BACKGROUND_COLOR_GAME)
game_title.pack()

# Set up window-block
game_window = Frame(master,
                    borderwidth=0, 
                    highlightthickness=0)
game_window.pack()

# Set up game-board background
canvas = Canvas(game_window, 
                height=SIZE_X, 
                width=SIZE_Y, 
                bg=BACKGROUND_COLOR_GAME,
                borderwidth=0, 
                highlightthickness=0)

canvas.pack(fill=BOTH, expand=False)
canvas.grid(row=4,column=4)

# ------------------------------- #
# Draw the empty board

def draw_cells(canvas, board):
    """
    Initialize the board colors
    """
    for indx in zip(range(GRID_LENGTH),range(GRID_LENGTH)):
        cell = Frame(canvas, 
                     bg=BACKGROUND_COLOR_CELL_EMPTY,
                     width=SIZE_X/GRID_LENGTH,
                     height=SIZE_Y/ GRID_LENGTH)
        cell.grid(row=indx[0]*int(SIZE_X/GRID_LENGTH), 
                  column=indx[1]*int(SIZE_Y/GRID_LENGTH), 
                  padx=GRID_PADDING,
                  pady=GRID_PADDING)
        cell.pack_propagate(0)
        txt = Label(master=cell,
                    text=,
                    bg=BACKGROUND_COLOR_CELL_EMPTY,
                    justify="center",
                    pady=5,
                    font=(GAME_FONT, GAME_FONT_SIZE, "bold"))
        txt.pack(expand=True)



draw_empty(canvas, GameBoard.board)


## Bind the keys
#master.bind("<Left>", moveleft)
#master.bind("<Right>", moveRight)
#master.bind("<Up>", moveUp)
#master.bind("<Down>", moveDown)
#master.bind("<a>", moveleft)
#master.bind("<d>", moveRight)
#master.bind("<w>", moveUp)
#master.bind("<s>", moveDown)


mainloop()
