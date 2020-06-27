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

# Plotting
import seaborn as sns
import matplotlib.pyplot as plt

action_dict = {0: "up", 1: "down", 2: "right", 3: "left"}

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
        q = [self.getQ(state, action_dict[a]) for a in self.actions]
        maxQ = max(q)

        if random.random() < self.epsilon:
            minQ = min(q); mag = max(abs(minQ), abs(maxQ))
            # add random values to all the actions, recalculate maxQ
            q = [q[i] + mag * (random.random() - 0.5)
                 for i in range(len(self.actions))] 
            maxQ = max(q)

        count = q.count(maxQ)
        # In case there're several state-action max values 
        # we select a random one among them
        if count > 1:
            best = [i for i in range(len(self.actions)) if q[i] == maxQ]
            i = random.choice(best)
        else:
            best = []
            i = q.index(maxQ)

        action = self.actions[i]
        print(i, action, len(best), q)
        if return_q: # if they want it, give it!
            return action, q
        return action

    def learn(self, state1, action1, reward, state2):
        maxqnew = max([self.getQ(state2, a) for a in self.actions])
        self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)

