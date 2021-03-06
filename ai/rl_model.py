#!/usr/bin/env python3

"""
2020.06.25 the Q function is not perfect yet
need to figure out how to pass states appropriately to the gym fxn

2020.06.24
Might want to look into turtle for the background

2020.06.23 

The following is using openai's gym RL 
on the 2048 rules from before.
"""

#Numerics
import numpy as np
import pandas as pd
import random

# RL Package
import gym
from gym import spaces
#import parameters as params
import ai.parameters as params

action_dict = {0: "up", 1: "down", 2: "right", 3: "left"}
flatten = lambda state: tuple(state.reshape(state.shape[0]**2))

class QLearn:
    def __init__(self, actions, epsilon, alpha, gamma):
        self.q = {}
        self.epsilon = epsilon  # exploration constant
        self.alpha = alpha      # discount constant
        self.gamma = gamma      # discount factor
        self.actions = actions

    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)

    def learnQ(self, state, action, reward, value):
        """
        Q-learning:
            Q(s, a) += alpha * (reward(s,a) + max(Q(s') - Q(s,a))            
        """
        oldv = self.q.get((state, action), None)

        if oldv is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)

    def chooseAction(self, state, return_q=False):
        """
        Exploration v. Optimality.

        If < epsilon - do a random action/explore
        if > epsilon - choose the optimal decision
        """
        state = flatten(state)
        q = [self.getQ(state, a) for a in self.actions]

        # Explore (A) or choose best action (B). If multiple
        # equally-good options exist for (B), then randomly choose one.
        if random.random() < self.epsilon:
            action = random.choice(self.actions)
        else:
            qmax = [idx for idx in range(len(self.actions)) if q[idx] == max(q)]
            action = random.choice(qmax)

        if return_q: # if they want it, give it!
            return action, q
        return action

    def learn(self, state1, action1, reward, state2):
        state1 = flatten(state1)
        state2 = flatten(state2)
        maxqnew = max([self.getQ(state2, a) for a in self.actions])
        self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)

class trainmodel:
    """
    """
    def __init__(self, env, alpha, epsilon, gamma):
        self.env = env
        self.qlearn = QLearn(actions=range(env.action_space.n), 
                             alpha=params.Alpha, 
                             gamma=params.Gamma, 
                             epsilon=params.Epsilon
                             )
        self.reset_env()
        self.frames = {0: {"state": env._get_observation(), 
                           "reward": 0, 
                           "action": 
                           "start", "game_over": False}}

    def reset_env(self):
        """ Re-initialize environment """
        self.env = self.env.reset()

