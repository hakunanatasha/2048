"""
Parameters for the RL agent.
"""

#Translate state-space into model readable actions
action_dict = {0: "up", 1: "down", 2: "right", 3: "left"}

# Number of times to play the game
N_episodes = 100 
seed = 1234

# Q-learning parameters
Alpha = 0.1
Gamma = 0.5
Epsilon = 0.9
