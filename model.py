#!/usr/bin/env python3
"""
2020.07.03
I'll initialize 2 types of training wherein
(1) Train for a fixed period of epoch moves 
(2) Train until the 2048 tile is created OR the game is over.

To do: make a text file that prints the success of each episode.

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

# Save files
#import gzip
import pickle as pkl

def run_model(env, qlearn, maxepoch=1e4, savetmp=None):
    """
    Training regime for models
    that train for a fixed episodic/epoch level

    env- pass RL environment
    qlearn - pass Q-learning

    maxepoch-stop training an episode after N (if None, trains until game condition met)
    savetmp - periodically save temp files. 
    """
    all_frames = []
    countr = 0
    score = 0

    if savetmp is not None:
        outputtxt = open(savetmp + "scores.txt", "w")

    for eps in range(params.N_episodes):
        print("Training episode = ", eps + 1)

        env.reset()

        frames = {0: {"state": env._get_observation(), 
              "reward": 0, 
              "action": 
              "start", "game_over": False}}

        done = False
        epoch = 0

        while not done:
            line = ["Ep:", eps+1, "epoch:", epoch+1, "Score", score, "Game status:", env.Game.game_over, "\n"]
            outputtxt.writelines("\t".join([str(i) for i in line]))

            currState = env._get_observation()
            action = qlearn.chooseAction(currState)
            # Updated state, new board score, reached 2048?, reward
            nextState, reward, done, score = env.step(action)
            qlearn.learn(currState, action, reward, nextState)

            frames.update({epoch: {
            'state': nextState,
            'action': params.action_dict[action],
            'reward': reward,
            'game_over': env.Game.game_over}
            })

            # Iterate the counters
            countr += 1
            epoch += 1

            if savetmp is not None and countr >= 100:
                countr = 0

                with open(savetmp + "qlearn_tmp.pkl", "wb") as f:
                    pkl.dump(qlearn, f)

                with open(savetmp + "states_tmp.pkl", "wb") as f:
                    pkl.dump(all_frames, f)

            if epoch >= maxepoch:
                done = True


        all_frames.append(frames)
        outputtxt.writelines("\n\n")

    print("All episodes completed")

    qname = "qlearn_eps" + str(params.N_episodes) + ".pkl"
    sname = "states_eps" + str(params.N_episodes) + ".pkl"
    
    with open(savetmp + qname, "wb") as f:
        pkl.dump(qlearn, f)

    with open(savetmp + sname, "wb") as f:
        pkl.dump(all_frames, f)

    outputtxt.close()
# --------------------- #

if __name__ == "__main__":

    #Save directory
    savedir = "data/"

    # Initialize a random seed for reproducibility
    random.seed(314159)
    np.random.seed(123)

    # Create the environment
    env = gym.make('gym_2048:game2048-v0')
    env.seed(456)
    env.action_space.seed(789)

    # Set-up learning algorithm
    qlearn = QLearn(actions=range(env.action_space.n), 
                    alpha=params.Alpha, 
                    gamma=params.Gamma, 
                    epsilon=params.Epsilon)

    run_model(env, qlearn, maxepoch=1e4, savetmp=savedir)

    #g = GameGrid(frames[0]['state'], traj, 1.5)
    #g.mainloop()