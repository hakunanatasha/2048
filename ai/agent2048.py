#!/usr/bin/env python3

"""
2020.06.26
Seems like the smart thing to do is run tkinter
mainloop on one thread, and send keyboard commands via another.
asyncio based on : 
<https://stackoverflow.com/a/47920128/4865723>


2020.06.25
This is a slight variant of the gui2048, but intended for
RL's gym to inherit.

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
import asyncio
import threading
import queue

# Game Aesthetics (all parameter), Game Mechanics
from game.constants import *
from game.rules import game2048

# Timing for movies
import time

# -------------- #
#tf = {False: "Continue", True:"Game Done"}

class GameGrid(Frame):
    """
    Inputs:
    board - the orientation of the board
    trajectory - dictionary of {step_id: [action, board, reward]}
    dt - sleep command to update board (in milliseconds)
    """
    def __init__(self, board, trajectory, dt):

        Frame.__init__(self)

        # Initiate threads
        self.queue = queue.Queue()

        # Set up the game layout
        self.master.title("2048")
        self.master.geometry(BOARD_SIZE)
        self.master.configure(bg=BACKGROUND_COLOR_GAME)

        # Setup the Game Scoreboard
        self.scoreboard_title = {True: "Game Over! ", False: ""}
        self.game_title = Label(self.master, 
                                text="Score=0", 
                                fg=TITLE_COLOR)
        self.update_scoreboard(score=0, 
                               action='Start', 
                               endboard=False)

        #Deploy movie
        #self.master.bind("<Key>", self.keystroke)

        #Set up the movie
        self.trajectory = trajectory
        self.Nframes = len(trajectory)
        self.dt = dt

        #Initialize the grid
        self.initialize_grid(board)
        self.run_thread()

    def refresh_data(self):
        """
        Move in a direction given a keystroke.
        """
        if not self.thread.is_alive() and self.queue.empty():
            return

        while not self.queue.empty():
            time.sleep(self.dt)
            key = self.queue.get()
            print("Queue Worked =", key)
            frame = self.trajectory[key] 
            self.update_grid(
                frame['state'], 
                frame['reward'], 
                frame['action'],
                frame['game_over']
            )
        #self.run_simulation(dt=self.dt)
    def run_thread(self):
        """
            Button-Event-Handler starting the asyncio part in a separate
            thread.
        """
        # create Thread object
        self.thread = AsyncioThread(self.queue, self.Nframes)

        #  timer to refresh the gui with data from the asyncio thread
        self.master.after(0, self.refresh_data)
        #self.master.after(self.dt, self.refresh_data)  # called only once!

        # start the thread
        self.thread.start()

    def initialize_grid(self, board):
        """ Create the default generated grid """
        self.game_window = Frame(self.master,
                            bg=BACKGROUND_COLOR_GAME,
                            height=SIZE_Y,
                            width=SIZE_X,
                            borderwidth=0, 
                            highlightthickness=0)
        self.game_window.pack()
        self.draw_cells(self.game_window, board)
        self.board = board

    def update_grid(self, board, score, action, game_over):
        """Update grid cells"""
        self.draw_cells(self.game_window, board)
        self.update_scoreboard(score=score, 
                             action=action, 
                             endboard=game_over)
        #self.update_idletasks()
        self.update()

    def update_scoreboard(self, score, action, endboard):
        """ Update scoreboard to include the score, and move taken """
        #self.score = score
        scorettl = self.scoreboard_title[endboard] + "Score=" + str(int(score)) + ', Action:' + action
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

    #def run_simulation(self, dt):
    #    """
    #    Given a trajectory,
    #    create a movie of the board
    #    """ 
    #    for epoch in self.trajectory.keys():
    #        frame = self.trajectory[epoch]
    #        while frame['game_over'] is False:
    #            self.master.after(dt*1000,
    #                     self.update_grid(frame['state'], 
    #                     frame['reward'], 
    #                     frame['action'],
    #                     frame['game_over']))
    #    #self.mainloop()

# ------------------------------- #

# Define the queue thread
class AsyncioThread(threading.Thread):
    def __init__(self, queue, Nframes):
        self.asyncio_loop = asyncio.get_event_loop()
        self.the_queue = queue
        self.Nframes = Nframes
        threading.Thread.__init__(self)

    def run(self):
        self.asyncio_loop.run_until_complete([
            self.the_queue.put(k) for k in range(self.Nframes)
        ])
        #self.asyncio_loop.run_until_complete(self.make_queue_commands())

    #async def make_queue_commands(self):
    #    """ Assign and order to each trajectory frame """
    #    tasks = [self.the_queue.put((k)) for k in range(self.Nframes)]
    #    #await asyncio.wait(tasks)


