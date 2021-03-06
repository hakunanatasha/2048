#!/usr/bin/env python3

"""
2020.06.22
Included the ability to 'remotely' play by entering in keystrokes
self.mainloop() is a blocking call
in order to leverage, you may need to .master.update() every iteration

2020.06.21

Tkinter playable 2048.

"""
import numpy as np
import sys
from itertools import product

from tkinter import *

# Game Aesthetics (all parameter), Game Mechanics
from constants import *
from rules import game2048

# -------------- #
#tf = {False: "Continue", True:"Game Done"}
class GameGrid(Frame):
    """
    """
    def __init__(self):

        Frame.__init__(self)

        # Call the mechanics of the game
        self.Game = game2048(GRID_LENGTH=GRID_LENGTH, 
                             MAX_POWER=MAX_POWER,
                             MAX_GEN=MAX_GEN)

        # Set up the game layout
        self.master.title("2048")
        self.master.geometry(BOARD_SIZE)
        self.master.configure(bg=BACKGROUND_COLOR_GAME)

        # Setup the Game Scoreboard
        self.scoreboard_ttl = {True: "Game Over! ", False: ""}
        self.game_title = Label(self.master, 
                                text="Score=" + str(self.Game.score), 
                                fg=TITLE_COLOR)
        self.update_scoreboard(endboard=False)

        # Key bindings
        self.master.bind("<Key>", self.keystroke)
        self.commands = commands

        #Initialize the Grid with 1 generated tile
        self.initialize_grid()

        # Deploy the game!
        self.mainloop()

    def initialize_grid(self):
        """ Create the default generated grid """
        self.game_window = Frame(self.master,
                            bg=BACKGROUND_COLOR_GAME,
                            height=SIZE_Y,
                            width=SIZE_X,
                            borderwidth=0, 
                            highlightthickness=0)
        self.game_window.pack()
        self.draw_cells(self.game_window, self.Game.board)

    def keystroke(self, event):
        """
        Move in a direction given a keystroke.
        """
        key = repr(event.char)
        if key in self.commands:
            self.Game.move_tiles(self.commands[key])
            #print(self.Game.board) # Dynamic view of the game board
            #print(self.Game.score) #Dynamic view of score
            #print(tf[self.Game.game_over])
            self.update_grid()
        #self.master.update()

    def update_grid(self):
        """Update grid cells"""
        self.draw_cells(self.game_window, self.Game.board)
        self.update_idletasks()
        self.update_scoreboard(endboard=self.Game.game_over)

    def update_scoreboard(self, endboard):
        scorettl = self.scoreboard_ttl[endboard] + "Score=" + str(int(self.Game.score)) 
        self.game_title.config(text=scorettl, 
                               font=(GAME_FONT, GAME_FONT_SIZE, "bold"),
                               bg=BACKGROUND_COLOR_GAME)
        self.game_title.pack()

    @staticmethod
    def draw_cells(canvas, board):
        """
        Given the tokens on the board
        associate the right numbers/colors

        TODO: This should be done as a single pass and iterated as an apply
        """
        xy = list(product(range(GRID_LENGTH), range(GRID_LENGTH)))
        # TODO: MAP APPLY
        for indx in xy:
            cell = Frame(canvas, 
                         bg=BACKGROUND_COLOR_DICT[board[indx[0], indx[1]]],
                         width=SIZE_X/GRID_LENGTH,
                         height=SIZE_Y/ GRID_LENGTH)
            cell.grid(row=indx[0]*int(SIZE_X/GRID_LENGTH), 
                      column=indx[1]*int(SIZE_Y/GRID_LENGTH), 
                      padx=GRID_PADDING,
                      pady=GRID_PADDING)
            cell.pack_propagate(0)
            txt = Label(master=cell,
                        text=TEXT_DICT[board[indx[0], indx[1]]],
                        bg=BACKGROUND_COLOR_DICT[board[indx[0], indx[1]]],
                        fg=TEXT_COLOR_DICT[board[indx[0], indx[1]]],
                        justify="center",
                        pady=2,
                        font=(GAME_FONT, GAME_FONT_SIZE, "bold"))
            txt.pack(expand=True)


# ------------------------------- #

# For interactive play, execute the game! This can be run in terminal
if __name__ == "__main__":
    GameGrid()



