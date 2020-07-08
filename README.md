# Winning strategies of 2048

*This is a work in progress!*

The goal of this project is to explore reinforcement learning strategies on the game 2048. 2048 is a game where on a 4 x 4 grid, you have the options of moving up/down/left/right in order to merge tiles, which are canonically multiples of 2. The goal is to merge enough tiles to create the infamous 2048 tile.\\

While there have been some interesting work on AI-techniques of 2048, this work often focuses on identifying high score/optimal score strategies. The following implementation hopes to address this question, along with another: "how do we face non-optimal choices?". In particular, there are many board configurations where *a priori*, we may not have the optimal choice. 

As I populate this project, I will be identifying different milestones.

At the moment, the implemented GUI version of the game works, as does a crude Q-learning approach to training. The model roughly plays 600 games/minute with Q-learning, but memory can become a problem after 44K games, as the state-dictionary can be quite enormous. 

## 2048 Game [game/]

Under this folder is the rules, constants, and GUI-variant of the game. The following files are as such:
+ ```rules.py```: Class to construct an instance of a playable 2048
+ ```constants.py```: Parameters to visualize the gameboard
+ ```gui2048.py```: A playable version of 2048.

To play an interactive version of the game, the command ```python game/gui2048.py``` should be sufficient. 

## Learning environment [gym-2048/]
To make the environment, cd into gym-2048 and pip install -e . in that directory.
These directories have the correct substructure to leverage gym, a python reinforcement learning tool. 

## Model AI [ai/]
This folder contains attributes to successfully train and implement a model with reinforcement learning. Currently, the only policy-training method implemented is Q-learning.
+ ```parameters.py```: parameters to train model
+ ```agent2048.py```: implementation to load environment and allow visualization of moves made
+ ```rl_model.py```: currently implemented Q-learning training objective.


## Credits
+ 2048 is a game made by Gabriele Cirulli. 
+ https://github.com/yangshun/2048-python has the appropriate color scheme/dimension game constants and employed this. 