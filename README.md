# Winning strategies of 2048

The goal of this project is to explore reinforcement learning strategies on the game 2048. 2048 is a game where on a 4 x 4 grid, you have the options of moving up/down/left/right in order to merge tiles, which are canonically multiples of 2. The goal is to merge enough tiles to create the infamous 2048 tile.\\

While there have been some interesting work on AI-techniques of 2048, they've focused on identifying the best possible high scores. While I am partially interested in that, I wanted to explore different reinforcement learning policies to ask the question "what do people do when faced with non-optimal decisions versus a machine"? In particular, many people play with the strategy which is to merge into an corner. There are game board designs that do not have an optimal direction to merge in the most immediate step (and there is an element of randomness in the generation of a new tile).

The first step of this exploration requires a functional version of the 2048 game. I wanted to code up something that was able to dynamically visualize the decisions a machine would take when playing this game. As of 2020.06.22, the tkinter-GUI approach works.

I borrowed https://github.com/yangshun/2048-python game constants.
## 2048 GUI Game


TODO:
XX 1. Construct 2048 code [NS + DKM]
2. Create policy
3. RL ontop
