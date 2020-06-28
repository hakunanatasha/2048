#!/usr/bin/env python3
"""
2020.06.27

The following setup trains an RL agent
and observes the moves the agent takes
via a visualization (GameGrid).
"""

#Numerics
import numpy as np
import pandas as pd
import random

# RL Package
import gym
import sys
from ai.agent2048 import GameGrid, AsyncioThread
import ai.parameters as params
from ai.rl_model import QLearn, action_dict

import asyncio
import threading
import random
import queue

#from ai.agent2048 import GameGrid
#import ai.parameters as params
#from ai.rl_model import QLearn, action_dict

# Plotting
#from sys import platform as sys_pf
#if sys_pf == 'darwin':
#    import matplotlib
#    matplotlib.use("TkAgg")

# Initialize a random seed for reproducibility
random.seed(314159)
np.random.seed(123)

# Create the environment
env = gym.make('gym_2048:game2048-v0', N_episodes=params.N_episodes)
env.seed(456)
env.action_space.seed(789)

# Set-up learning algorithm
qlearn = QLearn(actions=range(env.action_space.n), 
                alpha=params.Alpha, 
                gamma=params.Gamma, 
                epsilon=params.Epsilon)

# Begin training
# --------------------- #

all_frames = []
for Ntrain in range(5):
    print("Training episode", Ntrain + 1)
    #epoch = 0
    env.reset()
    frames = {0: {"state": env._get_observation(), 
              "reward": 0, 
              "action": 
              "start", "game_over": False}}
    done = False
    #while not done:
    while (epoch < 1e4) or (not done):
        print("Ep:", Ntrain+1, "epoch:", epoch+1)
        currState = env._get_observation()
        action = qlearn.chooseAction(currState)
        # Updated state, new board score, reached 2048?, reward
        nextState, score, done, reward = env.step(action)
        qlearn.learn(currState, action, reward, nextState)
        frames.update({epoch: {
        'state': nextState,
        'action': params.action_dict[action],
        'reward': reward,
        'game_over': env.Game.game_over}
        })
        #epoch += 1
    all_frames.append(frames)

# --------------------- #

#env.reset()
#frames = {0: {"state": env._get_observation(), 
#              "reward": 0, 
#              "action": 
#              "start", "game_over": False}}
#epochs = 1
#done = False
#while not done:
#    action = env.action_space.sample()
#    state, reward, done = env.step(action)
#    # Put each rendered frame into dict for animation
#    frames.update({epochs: {
#        'state': state,
#        'action': params.action_dict[action],
#        'reward': reward,
#        'game_over': env.Game.game_over,
#        }
#    })
#
#    epochs += 1
#
#traj = {idx: frames[idx] for idx in range(100)}

#g = GameGrid(frames[0]['state'], traj, 1.5)
#g.mainloop()

#for epoch in range(1):
#    observation = env.reset()
#    print("Initial State\n", observation)
#    done = False
#    while not done:
#        state = observation
#        action = env.action_space.sample()
#        state, reward, done, info = env.step(action)

        #action = qlearn.chooseAction(state, return_q=True)
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