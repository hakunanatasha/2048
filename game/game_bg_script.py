"""
2020.06.21

Tkinter playable 2048.

"""


from tkinter import *
from PIL import ImageTk, Image
import random
import numpy as np
import gameskin
from tkinter import messagebox
import sys

root = Tk()
root.title("2048")
root.geometry("500x600")

gameTitle = Label(root, text="2048", fg="#422568")
gameTitle.config(font=("Times New Roman", 50, "bold"))
gameTitle.pack()

gameWindow = Frame(root)
gameWindow.pack()

canvas = Canvas(gameWindow, height=400, width=400, bg='white')
canvas.pack(fill=BOTH, expand=False)

Board = np.zeros((4,4))

num0 = ImageTk.PhotoImage(Image.open("images/0.jpg"))
num2 = ImageTk.PhotoImage(Image.open("images/2.jpg"))
num4 = ImageTk.PhotoImage(Image.open("images/4.jpg"))
num8 = ImageTk.PhotoImage(Image.open("images/8.jpg"))
num16 = ImageTk.PhotoImage(Image.open("images/16.jpg"))
num32 = ImageTk.PhotoImage(Image.open("images/32.jpg"))
num64 = ImageTk.PhotoImage(Image.open("images/64.jpg"))
num128 = ImageTk.PhotoImage(Image.open("images/128.jpg"))
num256 = ImageTk.PhotoImage(Image.open("images/256.jpg"))
num512 = ImageTk.PhotoImage(Image.open("images/512.jpg"))
num1024 = ImageTk.PhotoImage(Image.open("images/1024.jpg"))
num2048 = ImageTk.PhotoImage(Image.open("images/2048.jpg"))

ImageNames = {
    0:num0,
    2:num2,
    4:num4,
    8:num8,
    16:num16,
    32:num32,
    64:num64,
    128:num128,
    256:num256,
    512:num512,
    1024:num1024,
    2048:num2048
}

score = 0

frame = LabelFrame(root, text="Score", padx=10, pady=10, labelanchor="n",font=("Arial", 20, "bold"),bd=5,width=60,fg="blue")
frame.pack()

scoreBoard = Label(frame, text=score, padx=15, pady=5,font=("Times New Roman",15))
scoreBoard.pack()

def get_x_y_coordinate(row, column):
    x = column * 100
    y = (3-row) * 100
    return x, y

def create_board():
    for row in range(4):
        for column in range(4):
            x1, y1= get_x_y_coordinate(row, column)
            x2, y2= x1 + 100, y1+100
            canvas.create_rectangle(x1, y1, x2, y2)

create_board()

def get_key(dict_name, val):
    for key, value in dict_name.items():
        if val == value:
            return key

def drawEmpty():
    for i in constants.positions.values():
        canvas.create_image(i, image=num0)

def isValid():
    for row in Board:
        for index in range(len(row)-1):
            if row[index] == row[index+1]:
                return True

    for column in range(4):
        row = Board[:, column]
        for index in range(len(row)-1):
            if row[index] == row[index+1]:
                return True

def updateScoreBoard():
    global scoreBoard
    scoreBoard.destroy()
    scoreBoard = Label(frame, text=score, padx=15, pady=5,font=("Times New Roman",15))
    scoreBoard.pack()

def gameOver():
    global Board
    response = messagebox.askyesno("Game Over", "Game Over, Play again?")
    if response == 1:
        Board = np.zeros((4,4))
        create_board()
        getStartBoard()
    else:
        sys.exit("Game Closed")

def placeRandomTile():
    try:
        randomVal = random.choice([2,4])
        blank = np.argwhere(Board == 0)
        randpos = random.choice(blank)
        x1, y1 = randpos
        Board[x1,y1] = randomVal
        val = randpos.tolist()
        pos = get_key(constants.BoardPos, val)
        canvas.create_image(constants.positions[pos], image=ImageNames[randomVal])
    except IndexError:
        if isValid():
            pass
        else:
            gameOver()



def getStartBoard():

    drawEmpty()

    randPos1 = random.choice(constants.y_axis_labels) + random.choice(constants.x_axis_labels)
    randNo1 = random.choice([2, 4])
    if randNo1 == 2:
        canvas.create_image(constants.positions[randPos1], image=num2)
    else:
        canvas.create_image(constants.positions[randPos1], image=num4)

    randPos2 = random.choice(constants.y_axis_labels) + random.choice(constants.x_axis_labels)
    if randPos1 == randPos2:
        randPos2 = random.choice(constants.y_axis_labels) + random.choice(constants.x_axis_labels)

    randNo2 = random.choice([2, 4])
    if randNo2 == 2:
        canvas.create_image(constants.positions[randPos2], image=num2)
    else:
        canvas.create_image(constants.positions[randPos2], image=num4)

    x1,y1 = constants.BoardPos[randPos1]
    x2,y2 = constants.BoardPos[randPos2]

    Board[x1,y1] = randNo1
    Board[x2,y2] = randNo2


getStartBoard()

def slide_row(row):
    global score
    nonzero = row[row!=0]
    if len(nonzero) == 4 and nonzero[0] == nonzero[1] and nonzero[2]== nonzero[3]:
        return np.array([nonzero[:2].sum(), nonzero[2:].sum(),0,0])
    for i in range(len(nonzero)-1):
        if nonzero[i] == nonzero[i+1]:
            score = int(score + nonzero[i] + nonzero[i+1])
            nonzero[i] += nonzero[i+1]
            nonzero[i+1] = 0
            nonzero = nonzero[nonzero!=0]
            break
    new_row = np.zeros(4)
    new_row[:len(nonzero)] = nonzero
    return new_row

def moveleft(Event):
    for row_index, row in enumerate(Board):
        newRow = slide_row(row)
        Board[row_index] = newRow

    for row_index,row in enumerate(Board):
        for index, element in enumerate(row):
            pos = get_key(constants.BoardPos, [row_index, index])
            canvas.create_image(constants.positions[pos], image=ImageNames[element])
    updateScoreBoard()
    placeRandomTile()

def moveRight(Event):
    for row_index, row in enumerate(Board):
        getrow = slide_row(row[::-1])
        newrow = getrow[::-1]
        Board[row_index] = newrow

    for row_index,row in enumerate(Board):
        for index, element in enumerate(row):
            pos = get_key(constants.BoardPos, [row_index, index])
            canvas.create_image(constants.positions[pos], image=ImageNames[element])
    updateScoreBoard()
    placeRandomTile()


def moveUp(Event):
    for column in range(4):
        row = Board[:, column]
        newrow = slide_row(row)
        Board[:, column] = newrow

    for row_index, row in enumerate(Board):
        for index, element in enumerate(row):
            pos = get_key(constants.BoardPos, [row_index, index])
            canvas.create_image(constants.positions[pos], image=ImageNames[element])
    updateScoreBoard()
    placeRandomTile()

def moveDown(Event):
    for column in range(4):
        row = Board[:, column]
        getrow = slide_row(row[::-1])
        newrow = getrow[::-1]
        Board[:, column] = newrow
    
    for row_index, row in enumerate(Board):
        for index, element in enumerate(row):
            pos = get_key(constants.BoardPos, [row_index, index])
            canvas.create_image(constants.positions[pos], image=ImageNames[element])
    updateScoreBoard()
    placeRandomTile()

root.bind("<Left>", moveleft)
root.bind("<Right>", moveRight)
root.bind("<Up>", moveUp)
root.bind("<Down>", moveDown)
root.bind("<a>", moveleft)
root.bind("<d>", moveRight)
root.bind("<w>", moveUp)
root.bind("<s>", moveDown)

root.mainloop()