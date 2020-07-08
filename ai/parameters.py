"""
Parameters for the RL agent.
"""

#Translate state-space into model readable actions
action_dict = {0: "up", 1: "down", 2: "right", 3: "left"}

# Number of times to play the game
N_episodes = 100000 
seed = 1234

# Q-learning parameters
Alpha = 0.1 # [0, 1]; importance of update
Gamma = 0.5 # [0, 1]; 0=> greedy, 1=>long term
Epsilon = 0.75 # Exploration (< eps) versus optimal choice (>= eps)
