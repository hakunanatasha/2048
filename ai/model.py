#!/usr/bin/env python3

#Numerics
import numpy as np
import pandas as pd
import random

# RL Package
import gym
import ai.parameters as params
from ai.rl_model import QLearn, action_dict

# Plotting
import seaborn as sns
import matplotlib.pyplot as plt

# Initialize a random seed for reproducibility
random.seed(314159)
np.random.seed(123)

# Create the environment

env = gym.make('gym_2048:game2048-v0', N_episodes=params.N_episodes)
env.seed(456)
env.action_space.seed(789)

# Set-up the q-learning
qlearn = QLearn(actions=range(env.action_space.n), 
                alpha=params.Alpha, 
                gamma=params.Gamma, 
                epsilon=params.Epsilon)

for epoch in range(1):
    observation = env.reset()
    print("Initial State\n", observation)
    done = False
    while not done:
        state = observation
        action = qlearn.chooseAction
#frames = []
#
#for epoch in range(5):
#    observation = env.reset()
#    done = False
#    while not done:
#        state = tuple(observation)  # turn np.ndarray into hashable type
#        action = qlearn.chooseAction(state)
#        observation, reward, done, info = env.step(action)
#        nextState = tuple(observation)  # turn np.ndarray into hashable type
#        qlearn.learn(state, action, reward-0*env.min_reward, nextState)
#        
#        frames.append({
#            'frame': env.render(mode='ansi'),
#            'state': state,
#            'action': action,
#            'reward': reward-0*env.min_reward,
#            'epoch': epoch
#        })